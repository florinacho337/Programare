import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.ShortBuffer;
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws Exception{
        short l1, l2;
        Scanner s = new Scanner(System.in);
        System.out.println("Introduceti o adresa si un port: ");
        String[] params = s.nextLine().split(" ");
        Socket c = new Socket(params[0], Integer.parseInt(params[1]));
        System.out.println("Introduceti lungimea primului sir: ");
        l1 = s.nextShort();
        System.out.println("Introduceti lungimea celui de-al doilea sir: ");
        l2 = s.nextShort();
        short[] sir1 = new short[l1];
        short[] sir2 = new short[l2];
        System.out.println("Introduceti elementele primului sir: ");
        for(int i = 0; i < l1; ++i){
            sir1[i] = s.nextShort();
        }
        System.out.println("Introduceti elementele celui de-al doilea sir: ");
        for(int i = 0; i < l2; ++i){
            sir2[i] = s.nextShort();
        }

        //create socketIn and socketOut
        DataInputStream socketIn = new DataInputStream(c.getInputStream());
        DataOutputStream socketOut = new DataOutputStream(c.getOutputStream());

        //write lengths
        socketOut.writeShort(l1);
        socketOut.writeShort(l2);

        //convert arrays
        ByteBuffer byteBuffer1 = ByteBuffer.allocate(sir1.length * 2);
        ByteBuffer byteBuffer2 = ByteBuffer.allocate(sir2.length * 2);
        ShortBuffer shortBuffer1 = byteBuffer1.asShortBuffer();
        ShortBuffer shortBuffer2 = byteBuffer2.asShortBuffer();
        shortBuffer1.put(sir1);
        shortBuffer2.put(sir2);
        byte[] array1 = byteBuffer1.array();
        byte[] array2 = byteBuffer2.array();

        

        //write arrays
        socketOut.write(array1);
        socketOut.write(array2);
        socketOut.flush();
        //read result;
        byte[] result = new byte[(l1+l2)*2];
        socketIn.read(result);

        //convert result
        ByteBuffer wrapped = ByteBuffer.wrap(result);
        short[] sir_interclasat = new short[l1+l2];
        for(int i = 0; i < l1+l2; ++i)
            sir_interclasat[i] = wrapped.getShort();

        System.out.println("Sirul interclasat este: ");
        System.out.println(Arrays.toString(sir_interclasat));
        s.close();
        c.close();
    }
}