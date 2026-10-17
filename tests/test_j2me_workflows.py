import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile

from scripts.j2me_compat_report import parse_class, report
from scripts.new_j2me_game import new_game


def synthetic_class():
    # Java 1.1 classfile, only constant-pool objects required by our scanner.
    pool = b"\x01" + struct.pack(">H",16) + b"java/lang/Object" + b"\x07\x00\x01"
    return b"\xca\xfe\xba\xbe"+struct.pack(">HHH",3,45,3)+pool


class J2MEWorkflows(unittest.TestCase):
    def test_constant_pool_and_class_version(self):
        decoded = parse_class(synthetic_class())
        self.assertEqual(decoded["major"],45)
        self.assertIn("java/lang/Object",decoded["classes"])

    def test_static_compat_report_reads_real_zip_without_executing(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"sample.jar"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("Game.class",synthetic_class())
                z.writestr("META-INF/MANIFEST.MF",
                    "MIDlet-Name: Test\nMIDlet-1: Test, , Game\n Micro\n")
            result=report(p)
            self.assertEqual(result["classes_inside_jar"],1)
            self.assertIn("java/lang/Object",result["external_api_classes"])
            self.assertFalse(result["claims"]["original_executed"])
            self.assertEqual(result["java_classfile_major_versions"][45],1)

    def test_generate_java_me_source_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)/"Game"
            new_game(base,"PocketCar","Pocket Car")
            self.assertIn("MIDP-2.0",(base/"MANIFEST.MF").read_text())
            self.assertIn("GameCanvas",(base/"src/pocketforge/PocketCarCanvas.java").read_text())
            self.assertIn("MIDlet",(base/"src/pocketforge/PocketCarMIDlet.java").read_text())
            with self.assertRaises(FileExistsError):new_game(base,"PocketCar","Pocket Car")

    def test_bad_classfile_and_name_rejected(self):
        with self.assertRaises(ValueError):parse_class(b"bad")
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):new_game(Path(td)/"bad","123-invalid","X")


if __name__ == "__main__":
    unittest.main()
