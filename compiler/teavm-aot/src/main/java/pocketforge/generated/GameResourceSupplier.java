package pocketforge.generated;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import org.teavm.classlib.ResourceSupplier;
import org.teavm.classlib.ResourceSupplierContext;

/** Build-only resource whitelist, generated from JAR entries, no game-specific logic. */
@SuppressWarnings("deprecation")
public final class GameResourceSupplier implements ResourceSupplier {
  public String[] supplyResources(ResourceSupplierContext context) {
    List<String> names = new ArrayList<String>();
    try (InputStream in = context.getClassLoader().getResourceAsStream("pocketforge-resource-index.txt")) {
      if (in == null) return new String[0];
      BufferedReader reader = new BufferedReader(new InputStreamReader(in, "UTF-8"));
      for (String line; (line = reader.readLine()) != null;) {
        if (!line.isEmpty() && !line.startsWith("#")) names.add(line);
      }
    } catch (Exception ex) {
      throw new IllegalStateException("Unable to read resource index", ex);
    }
    return names.toArray(new String[names.size()]);
  }
}
