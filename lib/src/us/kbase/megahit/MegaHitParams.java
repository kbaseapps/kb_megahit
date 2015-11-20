
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
 * <p>Original spec-file type: MegaHitParams</p>
 * <pre>
 * @optional megahit_parameter_preset
 * @optional min_count
 * @optional k_min
 * @optional k_max
 * @optional k_step
 * @optional k_list
 * @optional min_contig_length
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "read_library_name",
    "output_contigset_name",
    "megahit_parameter_preset",
    "min_count",
    "k_min",
    "k_max",
    "k_step",
    "k_list",
    "min_contig_length"
})
public class MegaHitParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("read_library_name")
    private String readLibraryName;
    @JsonProperty("output_contigset_name")
    private String outputContigsetName;
    @JsonProperty("megahit_parameter_preset")
    private String megahitParameterPreset;
    @JsonProperty("min_count")
    private java.lang.Long minCount;
    @JsonProperty("k_min")
    private java.lang.Long kMin;
    @JsonProperty("k_max")
    private java.lang.Long kMax;
    @JsonProperty("k_step")
    private java.lang.Long kStep;
    @JsonProperty("k_list")
    private List<Long> kList;
    @JsonProperty("min_contig_length")
    private java.lang.Long minContigLength;
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

    @JsonProperty("min_count")
    public java.lang.Long getMinCount() {
        return minCount;
    }

    @JsonProperty("min_count")
    public void setMinCount(java.lang.Long minCount) {
        this.minCount = minCount;
    }

    public MegaHitParams withMinCount(java.lang.Long minCount) {
        this.minCount = minCount;
        return this;
    }

    @JsonProperty("k_min")
    public java.lang.Long getKMin() {
        return kMin;
    }

    @JsonProperty("k_min")
    public void setKMin(java.lang.Long kMin) {
        this.kMin = kMin;
    }

    public MegaHitParams withKMin(java.lang.Long kMin) {
        this.kMin = kMin;
        return this;
    }

    @JsonProperty("k_max")
    public java.lang.Long getKMax() {
        return kMax;
    }

    @JsonProperty("k_max")
    public void setKMax(java.lang.Long kMax) {
        this.kMax = kMax;
    }

    public MegaHitParams withKMax(java.lang.Long kMax) {
        this.kMax = kMax;
        return this;
    }

    @JsonProperty("k_step")
    public java.lang.Long getKStep() {
        return kStep;
    }

    @JsonProperty("k_step")
    public void setKStep(java.lang.Long kStep) {
        this.kStep = kStep;
    }

    public MegaHitParams withKStep(java.lang.Long kStep) {
        this.kStep = kStep;
        return this;
    }

    @JsonProperty("k_list")
    public List<Long> getKList() {
        return kList;
    }

    @JsonProperty("k_list")
    public void setKList(List<Long> kList) {
        this.kList = kList;
    }

    public MegaHitParams withKList(List<Long> kList) {
        this.kList = kList;
        return this;
    }

    @JsonProperty("min_contig_length")
    public java.lang.Long getMinContigLength() {
        return minContigLength;
    }

    @JsonProperty("min_contig_length")
    public void setMinContigLength(java.lang.Long minContigLength) {
        this.minContigLength = minContigLength;
    }

    public MegaHitParams withMinContigLength(java.lang.Long minContigLength) {
        this.minContigLength = minContigLength;
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
        return ((((((((((((((((((((((("MegaHitParams"+" [workspaceName=")+ workspaceName)+", readLibraryName=")+ readLibraryName)+", outputContigsetName=")+ outputContigsetName)+", megahitParameterPreset=")+ megahitParameterPreset)+", minCount=")+ minCount)+", kMin=")+ kMin)+", kMax=")+ kMax)+", kStep=")+ kStep)+", kList=")+ kList)+", minContigLength=")+ minContigLength)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
