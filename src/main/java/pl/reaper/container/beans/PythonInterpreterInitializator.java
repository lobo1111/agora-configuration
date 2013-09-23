package pl.reaper.container.beans;

import java.io.File;
import javax.annotation.PostConstruct;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import org.python.core.PySystemState;

@Startup
@Singleton
public class PythonInterpreterInitializator {

    private String CACHE_DIR = "/opt/container/cache/";
    private File cacheDir = new File(CACHE_DIR);

    @PostConstruct
    public void init() {
        PySystemState.add_classdir("/opt/glassfish/domains/devel/applications/Container-0.1");
        for (File file : cacheDir.listFiles()) {
            if (file.delete()) {
                System.out.println("Cached file " + file.getName() + " deleted.");
            } else {
                System.out.println("Cached file " + file.getName() + " can't be deleted.");
            }
        }
    }
}
