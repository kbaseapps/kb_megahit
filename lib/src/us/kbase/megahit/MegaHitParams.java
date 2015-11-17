
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
 * <p>Original spec-file type: MegaHitParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "read_library_name",
    "megahit_parameter_preset",
    "output_contigset_name"
})
public class MegaHitParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("read_library_name")
    private String readLibraryName;
    @JsonProperty("megahit_parameter_preset")
    private String megahitParameterPreset;
    @JsonProperty("output_contigset_name")
    private String outputContigsetName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public MegaHitParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("read_library_name")
    public String getReadLibraryName() {
        return readLibraryName;
    }

    @JsonProperty("read_library_name")
    public void setReadLibraryName(String readLibraryName) {
        this.readLibraryName = readLibraryName;
    }

    public MegaHitParams withReadLibraryName(String readLibraryName) {
        this.readLibraryName = readLibraryName;
        return this;
    }

    @JsonProperty("megahit_parameter_preset")
    public String getMegahitParameterPreset() {
        return megahitParameterPreset;
    }

    @JsonProperty("megahit_parameter_preset")
    public void setMegahitParameterPreset(String megahitParameterPreset) {
        this.megahitParameterPreset = megahitParameterPreset;
    }

    public MegaHitParams withMegahitParameterPreset(String megahitParameterPreset) {
        this.megahitParameterPreset = megahitParameterPreset;
        return this;
    }

    @JsonProperty("output_contigset_name")
    public String getOutputContigsetName() {
        return outputContigsetName;
    }

    @JsonProperty("output_contigset_name")
    public void setOutputContigsetName(String outputContigsetName) {
        this.outputContigsetName = outputContigsetName;
    }

    public MegaHitParams withOutputContigsetName(String outputContigsetName) {
        this.outputContigsetName = outputContigsetName;
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
        return ((((((((((("MegaHitParams"+" [workspaceName=")+ workspaceName)+", readLibraryName=")+ readLibraryName)+", megahitParameterPreset=")+ megahitParameterPreset)+", outputContigsetName=")+ outputContigsetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
