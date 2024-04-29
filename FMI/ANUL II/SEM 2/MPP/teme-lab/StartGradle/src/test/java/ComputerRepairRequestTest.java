import ro.mpp2024.model.ComputerRepairRequest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import ro.mpp2024.repository.RequestRepository;

import java.util.stream.StreamSupport;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class ComputerRepairRequestTest {
    @Test
    @DisplayName("First Test")
    public void testeDomain(){
        ComputerRepairRequest computerRepairRequest = new ComputerRepairRequest();
        assertEquals("", computerRepairRequest.getOwnerName());
        computerRepairRequest.setModel("model");
        assertEquals("model", computerRepairRequest.getModel());
    }

    @Test
    @DisplayName("Second Test")
    public void teste2(){
        ComputerRepairRequest computerRepairRequest = new ComputerRepairRequest();
        RequestRepository repository = new RequestRepository();
        repository.add(computerRepairRequest);
        assertEquals(1, StreamSupport.stream(repository.findAll().spliterator(), false).toList().size());
    }
}