package ir.map.gr221;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static <E> void printArie(List<E> l, Arie<E> f){
        l.forEach(x -> System.out.println(f.compute(x)));
    }
    public static void main(String[] args) {

        Cerc cerc1 = new Cerc(2.0);
        Cerc cerc2 = new Cerc(3.0);

        List<Cerc> listaCercuri = Arrays.asList(cerc1, cerc2);

        Patrat patrat1 = new Patrat(1.0);
        Patrat patrat2 = new Patrat(2.0);

        List<Patrat> listaPatrate = Arrays.asList(patrat1, patrat2);

        Arie<Cerc> arieCerc = cerc -> Math.PI * cerc.getRaza() * cerc.getRaza();
        Arie<Cerc> arieCerc2 = (Cerc c) -> {
            return Math.PI * c.getRaza() * c.getRaza();
        };
//        Arie<Patrat> ariePatrat = patrat -> patrat.getLatura() * patrat.getLatura();
//        System.out.println(arieCerc.compute(cerc1));
//        System.out.println(arieCerc.compute(cerc2));
//        System.out.println(ariePatrat.compute(patrat1));
//        System.out.println(ariePatrat.compute(patrat2));

//        List<String> stringList = Arrays.asList("ab", "abc", "xyz", "mnpq", "aabbcc", "def");
//        stringList.forEach(str -> {
//            if (str.startsWith("a"))
//                System.out.println(str);
//        });
//
//        stringList.stream().filter(str -> str.startsWith("a")).forEach(System.out::println);

        List<Integer> stringList2 = Arrays.asList(1, 12, 17, 20, 2, 9);
//        stringList2.stream().filter("Aneluta"::startsWith).forEach(System.out::println);
        String concatenated = stringList2.stream()
                .map(Object::toString)
                .collect(Collectors.joining(", "));
        System.out.println(concatenated);
    }
}