
package us.kbase.megahit;

import java.util.HashMap;
import java.util.List;
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
    "console_out",
    "report"
})
public class MegaHitOutput {

    @JsonProperty("console_out")
    private List<String> consoleOut;
    @JsonProperty("report")
    private List<String> report;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("console_out")
    public List<String> getConsoleOut() {
        return consoleOut;
    }

    @JsonProperty("console_out")
    public void setConsoleOut(List<String> consoleOut) {
        this.consoleOut = consoleOut;
    }

    public MegaHitOutput withConsoleOut(List<String> consoleOut) {
        this.consoleOut = consoleOut;
        return this;
    }

    @JsonProperty("report")
    public List<String> getReport() {
        return report;
    }

    @JsonProperty("report")
    public void setReport(List<String> report) {
        this.report = report;
    }

    public MegaHitOutput withReport(List<String> report) {
        this.report = report;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((("MegaHitOutput"+" [consoleOut=")+ consoleOut)+", report=")+ report)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
