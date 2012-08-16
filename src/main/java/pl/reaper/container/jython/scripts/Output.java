package pl.reaper.container.jython.scripts;

public class Output {

    private String result = "";

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }
    
    public void appendResult(String result) {
        this.result += result;
    }
}
