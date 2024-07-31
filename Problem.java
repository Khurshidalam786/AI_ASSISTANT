import java.util.HashSet;
import java.util.Set;

class Problem {
    public static void main(String[] args) {
        int[] candy = {1, 1, 1, 1};
        Set<Integer> set = new HashSet<>();
        for (int i = 0; i < candy.length; i++) {
            set.add(candy[i]);
        }
        int maxCandyCanEat = candy.length / 2;
        if (set.size() <= maxCandyCanEat) {
            System.out.println(set.size());
        }
        else {
            System.out.println(maxCandyCanEat);
        }

    }
}
