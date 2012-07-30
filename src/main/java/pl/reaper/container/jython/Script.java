package pl.reaper.container.jython;

public class Script {

    private String script;
    private String onInit;
    private String name;

    public String getScript() {
        return script;
    }

    public void setScript(String script) {
        this.script = script;
    }

    public String getOnInit() {
        return onInit;
    }

    public void setOnInit(String onInit) {
        this.onInit = onInit;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
    
    @Override
    public String toString() {
        return name + "[" + script + "]";
    }
}
