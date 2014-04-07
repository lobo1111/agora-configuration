package pl.reaper.container.beans;

import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.LocalBean;
import javax.ejb.Schedule;
import javax.ejb.Singleton;
import javax.ejb.Startup;

@Singleton
@LocalBean
@Startup
public class ScriptsWatchdog {

    private final String instanceRoot = System.getProperty("com.sun.aas.instanceRoot");
    private final String watchPath = instanceRoot + File.separator + "container" + File.separator + "watchDir";
    private final String scriptReCompile = watchPath + File.separator + "recompile";
    @EJB
    private ScriptsLoaderLocal scriptsLoader;

    public void cleanWatchDir() {
        File dir = new File(watchPath);
        if (dir.exists()) {
            for (File file : dir.listFiles()) {
                checkFileDelete(file);
            }
        }
    }

    @Schedule(minute = "*", second = "0/10", dayOfMonth = "*", month = "*", year = "*", hour = "*", dayOfWeek = "*", info = "Script Watchdog", persistent = false)
    public void watchForReCompile() {
        Logger.getLogger(ScriptsWatchdog.class.getName()).log(Level.INFO, "Checking watchdir for scripts recompile...");
        File file = new File(scriptReCompile);
        if (file.exists()) {
            Logger.getLogger(ScriptsWatchdog.class.getName()).log(Level.INFO, "Scripts recompilation requested");
            scriptsLoader.compileScripts();
            checkFileDelete(file);
        } else {
            Logger.getLogger(ScriptsWatchdog.class.getName()).log(Level.INFO, "Scripts recompilation omitted");
        }
    }

    private void checkFileDelete(File file) {
        if (file.delete()) {
            Logger.getLogger(ScriptsWatchdog.class.getName()).log(Level.INFO, "File {0} deleted", file.getAbsolutePath());
        } else {
            Logger.getLogger(ScriptsWatchdog.class.getName()).log(Level.INFO, "File {0} NOT deleted", file.getAbsolutePath());
        }
    }
}
