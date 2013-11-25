import java.io.*;

class aligappl {

public static void main(String[] args) throws IOException {

Translator T = new Translator();
BufferedReader stream1 = new BufferedReader(new InputStreamReader(System.in));
String input1;

input1=stream1.readLine();
System.out.println(T.translateSentence(input1));

}

}