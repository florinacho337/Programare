package ir.map.g221;

import java.util.Comparator;
import java.util.HashSet;
import java.util.Objects;
import java.util.TreeSet;

public class Main {
    public static void main(String[] args) {
        Student s1 = new Student("Dan", 4.5f);
        Student s2 = new Student("Ana", 8.5f);
        Student s3 = new Student("Dan", 4.5f);

//        HashSet<Student> multime = new HashSet<>();
//        multime.add(s1);
//        multime.add(s2);
//        multime.add(s3);

        TreeSet<Student> multime = new TreeSet<>(new Comparator<Student>() {
            @Override
            public int compare(Student o1, Student o2) {
                return Float.compare(o1.getMedie(), o2.getMedie());
            }
        });
        multime.add(s1);
        multime.add(s2);
        multime.add(s3);


//        for (var elem : multime
//        ) {
//            System.out.println(elem);
//        }

        multime.forEach(System.out::println);
//        multime.forEach(x -> System.out.println(x));
//        multime.forEach(x -> x.setMedie(9));
    }
}