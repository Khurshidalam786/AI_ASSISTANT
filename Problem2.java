import java.util.Scanner;

public class Problem2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String text = sc.nextLine();
        sc.close();
        System.out.println("Total char : " + text.length());

        int spaceCount = 0;
        for (char c : text.toCharArray()) {
            if (c == ' ') {
                spaceCount++;
            }
        }

        System.out.println("Total spaces : " + spaceCount);

        text = text.replaceAll("\\s+", " ");
        String[] words = text.split(" ");
        System.out.println("Total number of words : " + words.length);
        for (String word : words) {
            System.out.println(word);
        }
    }
}
