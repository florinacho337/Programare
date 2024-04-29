package ro.mpp2024.network.jsonprotocol;

import com.google.gson.*;

import java.lang.reflect.Type;

public class ResponseTypeAdapter implements JsonDeserializer<ResponseType> {
    @Override
    public ResponseType deserialize(JsonElement jsonElement, Type type, JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {
        try {
            int ordinal = jsonElement.getAsInt();
            return ResponseType.values()[ordinal];
        } catch (NumberFormatException e) {
            return ResponseType.valueOf(jsonElement.getAsString());
        }
    }
}
