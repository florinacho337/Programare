package ro.mpp2024;

import ro.mpp2024.Car;
import ro.mpp2024.CarRepository;

import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;

public class MainBD {
    public static void main(String[] args) {

        Properties props=new Properties();
        try {
            props.load(new FileReader("bd.config"));
        } catch (IOException e) {
            System.out.println("Cannot find bd.config "+e);
        }

        Car car1 = new Car("Tesla","Model S", 2019);
        CarRepository carRepo=new CarsDBRepository(props);
        carRepo.add(car1);
        System.out.println("Toate masinile din db");
        for(Car car:carRepo.findAll())
            System.out.println(car);
        String manufacturer="Tesla";
        System.out.println("Masinile produse de "+manufacturer);
        for(Car car:carRepo.findByManufacturer(manufacturer))
            System.out.println(car);


        carRepo.update(4, new Car("Tesla", "Model 3", car1.getYear() + 1));
        System.out.println("Masinile produse de " + manufacturer);
        for(Car car:carRepo.findByManufacturer(manufacturer))
            System.out.println(car);

        int min = 2000;
        int max = 2010;
        System.out.println("Modelele aflate intre anii " + min + " si " + max);
        for (Car car:carRepo.findBetweenYears(min, max))
            System.out.println(car);

    }
}
