package pl.reaper.container.jython;

import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class VariableParser {

    private String toParse;
    private Map<String, String> variables;

    public VariableParser(String toParse, Map variables) {
        this.toParse = toParse;
        this.variables = variables;
    }

    public String parse() throws StringIndexOutOfBoundsException {
        StringBuilder result = new StringBuilder();
        Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "Parsing string: {0}", toParse);
        int previousEndMarker = 0;
        int from;
        int to;
        while ((from = toParse.indexOf("[:", previousEndMarker)) > -1 && (to = toParse.indexOf("]", previousEndMarker)) > -1) {
            Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "Found variable at {0}-{1}", new Object[]{from, to});
            String toReplace = toParse.substring(from + 2, to);
            Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "Replacing {0}", toReplace);
            if (variables.containsKey(toReplace)) {
                Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "Variable found, inserting {0}", variables.get(toReplace));
                result.append(toParse.substring(previousEndMarker, from)).append(String.valueOf(variables.get(toReplace)));
            } else {
                Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "Variable not found, inserting {0}", toReplace);
                result.append(toParse.substring(previousEndMarker, from)).append("[:").append(toReplace).append("]");
            }
            previousEndMarker = to + 1;
        }
        result.append(toParse.substring(previousEndMarker, toParse.length()));
        Logger.getLogger(VariableParser.class.getName()).log(Level.FINE, "String parsed: {0}", result.toString());
        return result.toString();
    }
}
