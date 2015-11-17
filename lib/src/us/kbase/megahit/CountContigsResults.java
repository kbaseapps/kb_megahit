
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
 * <p>Original spec-file type: CountContigsResults</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "contig_count"
})
public class CountContigsResults {

    @JsonProperty("contig_count")
    private Long contigCount;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("contig_count")
    public Long getContigCount() {
        return contigCount;
    }

    @JsonProperty("contig_count")
    public void setContigCount(Long contigCount) {
        this.contigCount = contigCount;
    }

    public CountContigsResults withContigCount(Long contigCount) {
        this.contigCount = contigCount;
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
        return ((((("CountContigsResults"+" [contigCount=")+ contigCount)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
