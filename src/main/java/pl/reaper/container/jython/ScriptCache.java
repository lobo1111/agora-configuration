package pl.reaper.container.jython;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ScriptCache {

    private String CACHE_DIR = "/opt/container/cache/";
    private File cacheDir = new File(CACHE_DIR);

    private boolean isCacheDirAvailable() {
        return cacheDir.exists() && cacheDir.isDirectory();
    }

    public boolean inCache(final String scriptName) {
        return isCacheDirAvailable() && cacheDir.listFiles(new FilenameFilter() {
            @Override
            public boolean accept(File dir, String name) {
                return name.substring(0, name.lastIndexOf(".")).equals(scriptName);
            }
        }).length == 1;
    }

    public String getFromCache(final String scriptName) {
        if (isCacheDirAvailable()) {
            File[] fileList = cacheDir.listFiles(new FilenameFilter() {
                @Override
                public boolean accept(File dir, String name) {
                    return name.substring(0, name.lastIndexOf(".")).equals(scriptName);
                }
            });
            if (fileList.length == 1) {
                return content(fileList[0]);
            } else {
                return null;
            }
        } else {
            return null;
        }
    }

    public void cache(String scriptName, String scriptContent) {
        if (isCacheDirAvailable() && !inCache(scriptName)) {
            try {
                try (FileWriter writer = new FileWriter(CACHE_DIR + scriptName + ".py")) {
                    writer.write(scriptContent);
                }
            } catch (IOException ex) {
                Logger.getLogger(ScriptCache.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    private String content(File file) {
        String script = "";
        char buffer[] = new char[4096];
        int read;
        try {
            FileReader reader = new FileReader(file);
            while ((read = reader.read(buffer)) != -1) {
                script += String.copyValueOf(buffer, 0, read);
            }
        } catch (IOException ex) {
            Logger.getLogger(ScriptCache.class.getName()).log(Level.SEVERE, null, ex);
        }
        return script;
    }
}
