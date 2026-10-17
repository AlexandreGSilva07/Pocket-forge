"""Deterministic, offline Standard MIDI File discovery and SoundFont rendering.

Not tied to any J2ME title: discovers MIDI streams inside JAR resources,
including proprietary concatenated resource banks, validates their boundaries,
and synthesizes them with a local General MIDI SoundFont via libfluidsynth.
Synthesized audio is packed as Ogg/Opus in the AOT output. No synth binaries,
SoundFonts, JARs, or remote resources are included in browser output.
"""
from __future__ import annotations
import ctypes
import ctypes.util
import io
import os
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path

MAX_SONGS = 48
MAX_MIDI_BYTES = 2 * 1024 * 1024
MAX_DURATION = 360
SAMPLE_RATE = 22050

@dataclass(frozen=True)
class MidiEvent:
    tick: int
    kind: str
    channel: int
    data1: int
    data2: int = 0

def _variable(data: bytes, offset: int, end: int) -> tuple[int,int]:
    v=0
    for _ in range(4):
        if offset>=end:raise ValueError("Truncated MIDI variable-length quantity")
        b=data[offset];offset+=1
        v=(v<<7)|(b&127)
        if not (b&128):return v,offset
    raise ValueError("MIDI variable length exceeds four bytes")

def _parse_song(data: bytes) -> tuple[list[tuple[float,MidiEvent]],float]:
    if len(data)<14 or data[:4]!=b"MThd":raise ValueError("Not SMF")
    nheader=struct.unpack_from(">I",data,4)[0]
    if nheader!=6 or 8+nheader>len(data):raise ValueError("Unsupported MIDI header")
    fmt,nt,division=struct.unpack_from(">HHH",data,8)
    if fmt not in (0,1) or nt<1 or nt>64 or (division&0x8000) or division==0:
        raise ValueError("Unsupported MIDI format, tracks, or SMPTE timing")
    offset=14;events=[];order=0;endtick=0
    for track in range(nt):
        if offset+8>len(data) or data[offset:offset+4]!=b"MTrk":
            raise ValueError("Missing MIDI track")
        track_size=struct.unpack_from(">I",data,offset+4)[0]
        offset+=8
        end=offset+track_size
        if end>len(data):raise ValueError("Incomplete MIDI track")
        tick=0;last_status=0;maxevents=0
        while offset<end:
            delta,offset=_variable(data,offset,end)
            tick+=delta
            endtick=max(endtick,tick)
            if offset>=end:raise ValueError("Missing MIDI event")
            initial=data[offset]
            if initial&0x80:
                status=initial;offset+=1
                if status<0xF0:last_status=status
            else:
                if not (0x80<=last_status<0xF0):raise ValueError("Invalid running status")
                status=last_status
            if status==0xFF:
                if offset>=end:raise ValueError("Missing MIDI meta type")
                subtype=data[offset];offset+=1
                size,offset=_variable(data,offset,end)
                if size>end-offset:raise ValueError("Truncated MIDI meta")
                if subtype==0x51 and size==3:
                    micros=int.from_bytes(data[offset:offset+3],"big")
                    if micros>0:events.append((tick,order,MidiEvent(tick,"tempo",0,micros)))
                offset+=size
                if subtype==0x2F: # keep reading to declared track boundary
                    offset=end
            elif status in (0xF0,0xF7):
                size,offset=_variable(data,offset,end)
                if size>end-offset:raise ValueError("Truncated sysex")
                offset+=size
            elif status<0xF0:
                kind=status&0xF0;ch=status&15
                needed=1 if kind in (0xC0,0xD0) else 2
                if offset+needed>end:raise ValueError("Truncated channel event")
                d1=data[offset];d2=data[offset+1] if needed==2 else 0
                if d1>127 or d2>127:raise ValueError("Invalid MIDI data byte")
                offset+=needed
                if kind==0x80:label="off"
                elif kind==0x90:label="on" if d2 else "off"
                elif kind==0xB0:label="cc"
                elif kind==0xC0:label="prog"
                elif kind==0xE0:label="bend"
                else:label="other"
                if label!="other":
                    events.append((tick,order,MidiEvent(tick,label,ch,d1,d2)))
            else:
                raise ValueError(f"Unsupported MIDI status 0x{status:x}")
            order+=1;maxevents+=1
            if maxevents>200000:raise ValueError("MIDI event budget exceeded")
        offset=end
    if offset!=len(data):raise ValueError("Unexpected MIDI trailing content")
    events.sort(key=lambda x:(x[0],x[1]))
    tempo=500000
    lasttick=0;now=0.0;absolute=[]
    for tick,_,event in events:
        now+=(tick-lasttick)*tempo/(division*1000000)
        lasttick=tick
        absolute.append((now,event))
        if event.kind=="tempo":tempo=event.data1
    final=now+(endtick-lasttick)*tempo/(division*1000000)
    return absolute,final

def find_midi_resources(resources: dict[str,bytes])->dict[bytes,str]:
    result={}
    for name,blob in resources.items():
        at=0
        while len(result)<MAX_SONGS:
            start=blob.find(b"MThd",at)
            if start<0:break
            at=start+4
            if start+14>len(blob):break
            header_size=struct.unpack_from(">I",blob,start+4)[0]
            if header_size!=6:continue
            ntracks=struct.unpack_from(">H",blob,start+10)[0]
            if ntracks<1 or ntracks>64:continue
            p=start+14;ok=True
            for _ in range(ntracks):
                if p+8>len(blob) or blob[p:p+4]!=b"MTrk":
                    ok=False;break
                sz=struct.unpack_from(">I",blob,p+4)[0]
                p+=8+sz
                if p>len(blob) or p-start>MAX_MIDI_BYTES:
                    ok=False;break
            if not ok:continue
            raw=blob[start:p]
            try:_parse_song(raw)
            except ValueError:continue
            result[raw]=f"{name}@{start}"
            at=p
    return result

class FluidSynth:
    def __init__(self,sf2:Path,rate:int=SAMPLE_RATE):
        path=ctypes.util.find_library("fluidsynth")
        if not path:raise RuntimeError("libfluidsynth is needed for offline MIDI rendering")
        self.dll=ctypes.CDLL(path)
        def bind(name,restype,*argtypes):
            f=getattr(self.dll,name);f.restype=restype;f.argtypes=argtypes;return f
        ptr=ctypes.c_void_p;int_=ctypes.c_int
        self.settings=bind("new_fluid_settings",ptr)()
        if not self.settings:raise RuntimeError("FluidSynth settings failed")
        self._delete_settings=bind("delete_fluid_settings",None,ptr)
        bind("fluid_settings_setnum",int_,ptr,ctypes.c_char_p,ctypes.c_double)(self.settings,b"synth.sample-rate",rate)
        bind("fluid_settings_setnum",int_,ptr,ctypes.c_char_p,ctypes.c_double)(self.settings,b"synth.gain",0.3)
        bind("fluid_settings_setint",int_,ptr,ctypes.c_char_p,int_)(self.settings,b"synth.reverb.active",0)
        bind("fluid_settings_setint",int_,ptr,ctypes.c_char_p,int_)(self.settings,b"synth.chorus.active",0)
        self.synth=bind("new_fluid_synth",ptr,ptr)(self.settings)
        if not self.synth:raise RuntimeError("FluidSynth constructor failed")
        self._delete_synth=bind("delete_fluid_synth",None,ptr)
        sf_id=bind("fluid_synth_sfload",int_,ptr,ctypes.c_char_p,int_)(self.synth,os.fsencode(sf2),1)
        if sf_id<0:raise RuntimeError("Cannot load MIDI SoundFont: "+str(sf2))
        self.note_on=bind("fluid_synth_noteon",int_,ptr,int_,int_,int_)
        self.note_off=bind("fluid_synth_noteoff",int_,ptr,int_,int_)
        self.program=bind("fluid_synth_program_change",int_,ptr,int_,int_)
        self.cc=bind("fluid_synth_cc",int_,ptr,int_,int_,int_)
        self.bend=bind("fluid_synth_pitch_bend",int_,ptr,int_,int_)
        self.alloff=bind("fluid_synth_all_sounds_off",int_,ptr,int_)
        self.write=bind("fluid_synth_write_s16",int_,ptr,int_,ptr,int_,int_,ptr,int_,int_)
        self.rate=rate
    def close(self):
        if self.synth:self._delete_synth(self.synth);self.synth=None
        if self.settings:self._delete_settings(self.settings);self.settings=None
    def __enter__(self):return self
    def __exit__(self,*args):self.close()

    def render(self,midi:bytes,codec:str="libopus")->bytes:
        events,duration=_parse_song(midi)
        if duration>MAX_DURATION:
            raise ValueError(f"MIDI exceeds {MAX_DURATION}s build-time cap")
        if not shutil.which("ffmpeg"):raise RuntimeError("ffmpeg required for MIDI compression")
        args=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-f","s16le",
              "-ar",str(self.rate),"-ac","2","-i","pipe:0","-c:a",codec,
              "-b:a","64k","-application","audio","-f","ogg","pipe:1"]
        # Limit tail so note releases sound natural but do not add long silence.
        totalframes=int((duration+1.25)*self.rate)
        raw=io.BytesIO()
        curframe=0
        def emit(length):
            while length:
                n=min(length,4096)
                buf=(ctypes.c_short*(2*n))()
                addr=ctypes.cast(buf,ctypes.c_void_p)
                if self.write(self.synth,n,addr,0,2,addr,1,2)!=0:
                    raise RuntimeError("FluidSynth rendering failed")
                raw.write(bytes(buf))
                length-=n
        try:
            for at,event in events:
                target=min(totalframes,round(at*self.rate))
                if target>curframe:
                    emit(target-curframe);curframe=target
                kind=event.kind
                if kind=="on":self.note_on(self.synth,event.channel,event.data1,event.data2)
                elif kind=="off":self.note_off(self.synth,event.channel,event.data1)
                elif kind=="prog":self.program(self.synth,event.channel,event.data1)
                elif kind=="cc":self.cc(self.synth,event.channel,event.data1,event.data2)
                elif kind=="bend":self.bend(self.synth,event.channel,(event.data2<<7)|event.data1)
            emit(max(0,totalframes-curframe))
            proc=subprocess.run(args,input=raw.getvalue(),capture_output=True,timeout=90)
            if proc.returncode:
                raise RuntimeError("ffmpeg Ogg/Opus MIDI encode failed: "+proc.stderr.decode(errors="replace")[-800:])
            return proc.stdout
        finally:
            for ch in range(16):self.alloff(self.synth,ch)

def default_soundfont()->Path|None:
    for p in [
        "/usr/share/sounds/sf2/TimGM6mb.sf2",
        "/usr/share/sounds/sf2/default-GM.sf2",
        "/usr/share/soundfonts/default.sf2",
    ]:
        path=Path(p)
        if path.is_file():return path
    return None
