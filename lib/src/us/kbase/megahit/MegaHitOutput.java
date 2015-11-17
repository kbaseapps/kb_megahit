
package us.kbase.megahit;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MegaHitOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "console_out"
})
public class MegaHitOutput {

    @JsonProperty("console_out")
    private String consoleOut;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("console_out")
    public String getConsoleOut() {
        return consoleOut;
    }

    @JsonProperty("console_out")
    public void setConsoleOut(String consoleOut) {
        this.consoleOut = consoleOut;
    }

    public MegaHitOutput withConsoleOut(String consoleOut) {
        this.consoleOut = consoleOut;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("MegaHitOutput"+" [consoleOut=")+ consoleOut)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
