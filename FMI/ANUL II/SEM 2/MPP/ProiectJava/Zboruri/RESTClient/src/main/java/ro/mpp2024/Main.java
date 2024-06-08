package ro.mpp2024;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.cfg.MapperConfig;
import com.fasterxml.jackson.databind.introspect.AnnotatedField;
import com.fasterxml.jackson.databind.introspect.AnnotatedMethod;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.utils.Constants;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;


public class Main {
    private static final String URL = "http://localhost:5198/api/zboruri";

    public List<Zbor> getAll() {
        Response response = RestAssured.get(URL);
        return Arrays.asList(response.as(Zbor[].class));
    }

    public List<Zbor> getAllByDestDateAndMinSeats(String destinatie, LocalDateTime date, int minSeats) {
        Response response = RestAssured.get(URL + "/filter?dest=" + destinatie + "&date=" + Constants.DATE_FORMATTER.format(date) + "&minSeats=" + minSeats);
        return Arrays.asList(response.as(Zbor[].class));
    }

    public Zbor getById(int id) {
        Response response = RestAssured.get(URL + "/" + id);
        return response.as(Zbor.class);
    }

    public Zbor create(Zbor zbor) throws JsonProcessingException {
        RequestSpecification request = RestAssured.given();
        request.header("Content-Type", "application/json");
        String zborJson = createZborJson(zbor);
        System.out.println(zborJson);
        request.body(zborJson);
        Response response = request.post(URL);
        return response.as(Zbor.class);
    }

    public void update(int id, Zbor zbor) throws JsonProcessingException {
        RequestSpecification request = RestAssured.given();
        request.header("Content-Type", "application/json");
        String zborJson = createZborJson(zbor);
        request.body(zborJson);
        request.put(URL + "/" + id);
        System.out.println("Updated successfully!");
    }

    private String createZborJson(Zbor zbor) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);

        SimpleModule module = new SimpleModule();
        module.addSerializer(LocalDateTime.class, new StdSerializer<>(LocalDateTime.class) {
            @Override
            public void serialize(LocalDateTime value, JsonGenerator gen, SerializerProvider provider) throws IOException {
                gen.writeString(Constants.DATE_TIME_FORMATTER_JSON.format(value));
            }
        });

        mapper.registerModule(module);
        return mapper.writeValueAsString(zbor);
    }

    public void delete(int id) {
        RestAssured.delete(URL + "/" + id);
        System.out.println("Deleted successfully!");
    }

    public static void main(String[] args) throws JsonProcessingException {
        Main client = new Main();

        List<Zbor> zboruri = client.getAll();
        System.out.println("Zboruri: " + zboruri);

        List<Zbor> zboruriFiltered = client.getAllByDestDateAndMinSeats("Amsterdam", LocalDateTime.parse("2024-09-13T00:00"), 3);
        System.out.println("Zboruri filtrate: " + zboruriFiltered);

        Zbor zbor = client.getById(1);
        System.out.println("Zbor gasit: " + zbor);

        Zbor newZbor = new Zbor("Aeroport1", "Destinatie1", LocalDateTime.now(), 100);
        Zbor createdZbor = client.create(newZbor);
        System.out.println("Zbor creat: " + createdZbor);

        createdZbor.setAeroport("UpdatedAeroport");
        client.update(createdZbor.getId(), createdZbor);

        client.delete(createdZbor.getId());
    }

}