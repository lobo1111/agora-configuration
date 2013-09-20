package pl.reaper.container.beans;

import java.util.Properties;
import javax.annotation.PostConstruct;
import javax.ejb.LocalBean;
import javax.ejb.Startup;
import javax.ejb.Stateless;
import org.python.util.PythonInterpreter;

@Stateless
@LocalBean
@Startup
public class PythonInterpreterInitializator {

    @PostConstruct
    public void init() {
        Properties properties = new Properties();
        properties.setProperty("python.path", "/usr/share/jython/Lib");
        PythonInterpreter.initialize(System.getProperties(), properties, new String[]{});
        System.out.println("PythonInterpreter initialized.");
    }
}
