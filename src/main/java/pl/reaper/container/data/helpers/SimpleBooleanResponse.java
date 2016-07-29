package pl.reaper.container.data.helpers;

public class SimpleBooleanResponse {

    private boolean value;

    public SimpleBooleanResponse(boolean value) {
        this.value = value;
    }

    public boolean isValue() {
        return value;
    }

    public void setValue(boolean value) {
        this.value = value;
    }
}
