package pl.reaper.container.jython;

import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.SessionContext;
import javax.script.ScriptException;
import pl.reaper.container.beans.JythonAuthenticatorLocal;
import pl.reaper.container.data.Dictionary;
import pl.reaper.container.data.Script;

public class ScriptExecutor {

    private ScriptLoader loader;
    private ScriptEngineWrapper engineBuilder;
    private SessionContext sessionContext;
    private boolean preservePrivilages = true;
    private JythonAuthenticatorLocal authenticator;

    private Object executeScripts(List<Script> scripts, Map variables) {
        try {
            engineBuilder.addVariables(variables);
            for (Script script : scripts) {
                checkSecurity(script);
                engineBuilder.addVariable("_scriptId", script.getId());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                engineBuilder.eval(script.getScript());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            return engineBuilder.eval(scripts.get(scripts.size() - 1).getOnInit());
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, "Script execution exception[[" + engineBuilder.getLastExecuted() + "]]", ex);
            return ex.getMessage();
        }
    }

    public String fire(String name, Map variables) {
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing script: {0}", name);
        String result = String.valueOf(executeScripts(loader.loadScriptChain(name), variables));
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script executed, result: {0}...", result.substring(0, 100));
        return result;
    }

    private void checkSecurity(Script script) throws ScriptException {
        if (sessionContext == null || !preservePrivilages) {
            return;
        } else {
            for (Dictionary group : script.getAllowedGroups()) {
                if (authenticator.isUserInRole(sessionContext.getCallerPrincipal().getName(), group.getKey())) {
                    return;
                }
            }
        }
        throw new ScriptException("You are not authorized to execute this script[id:" + script.getId() + "][name:" + script.getName() + "]");
    }

    public void setLoader(ScriptLoader loader) {
        this.loader = loader;
    }

    public void setEngineBuilder(ScriptEngineWrapper engineBuilder) {
        this.engineBuilder = engineBuilder;
    }

    public void setSessionContext(SessionContext sessionContext) {
        this.sessionContext = sessionContext;
    }

    public void setPreservePrivilages(boolean preservePrivilages) {
        this.preservePrivilages = preservePrivilages;
    }
    
    public void setAuthenticator(JythonAuthenticatorLocal authenticator) {
        this.authenticator = authenticator;
    }

}
