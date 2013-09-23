package pl.reaper.container.beans;

import java.io.File;
import java.util.Properties;
import javax.annotation.PostConstruct;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import org.python.util.PythonInterpreter;

@Startup
@Singleton
public class PythonInterpreterInitializator {

    @PostConstruct
    public void init() {
        String CACHE_DIR = "/opt/container/cache/";
        File cacheDir = new File(CACHE_DIR);
        Properties properties = new Properties();
        properties.setProperty("python.path", "/usr/share/jython/Lib");
        PythonInterpreter.initialize(System.getProperties(), properties, new String[]{});
        for (File file : cacheDir.listFiles()) {
            if (file.delete()) {
                System.out.println("Cached file " + file.getName() + " deleted.");
            } else {
                System.out.println("Cached file " + file.getName() + " can't be deleted.");
            }
        }
        System.out.println("PythonInterpreter initialized.");
    }
}
