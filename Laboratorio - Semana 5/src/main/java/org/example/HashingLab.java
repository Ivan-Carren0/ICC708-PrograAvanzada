package org.example;
import java.util.*;

public class HashingLab {

    static class Pair {
        String key;
        int value;
        Pair(String k, int v) { key = k; value = v; }
    }

    static class HashTableChaining {
        List<List<Pair>> table;
        int size, count, collisions;
        String hashStrategy;

        HashTableChaining(int size, String strategy) {
            this.size = size;
            this.count = 0;
            this.collisions = 0;
            this.hashStrategy = strategy;
            table = new ArrayList<>();
            for (int i = 0; i < size; i++) table.add(new LinkedList<>());
        }

        int hashSum(String key) {
            int sum = 0;
            for (char c : key.toCharArray()) sum += c;
            return sum % size;
        }

        int hashPolynomial(String key) {
            int h = 0;
            for (char c : key.toCharArray()) h = (h * 31 + c) % size;
            return h;
        }

        private int hash(String key) {
            if (hashStrategy.equals("sum")) {
                return hashSum(key);
            } else if (hashStrategy.equals("polynomial")) {
                return hashPolynomial(key);
            }
            throw new IllegalArgumentException("Unknown hash hashStrategy");
        }

        void insert(String key, int value) {
            int pos = hash(key);
            List<Pair> bucket = table.get(pos);

            for (Pair p : bucket) {
                if (p.key.equals(key)) { p.value = value; return; }
            }
            if (!bucket.isEmpty()) collisions++;
            bucket.add(new Pair(key, value));
            count++;
        }

        Integer search(String key) {
            int pos = hash(key);
            for (Pair p : table.get(pos)) {
                if (p.key.equals(key)) return p.value;
            }
            return null;
        }

        boolean delete(String key) {
            int pos = hash(key);
            List<Pair> bucket = table.get(pos);
            for (int i = 0; i < bucket.size(); i++) {
                if (bucket.get(i).key.equals(key)) {
                    bucket.remove(i);
                    count--;
                    return true;
                }
            }
            return false;
        }

        public double loadFactor() {
            return (double) count / size;
        }

        public int usedBuckets() {
            int used = 0;
            for (List<Pair> bucket : table) {
                if (!bucket.isEmpty()) used++;
            }
            return used;
        }

        public int maxBucketSize() {
            int max = 0;
            for (List<Pair> bucket : table) {
                max = Math.max(max, bucket.size());
            }
            return max;
        }

        public void printReport(double elapsedSeconds) {
            System.out.println("hashStrategy=" + hashStrategy
                    + ", size=" + size
                    + ", elements=" + count
                    + ", loadFactor=" + String.format("%.3f", loadFactor())
                    + ", collisions=" + collisions
                    + ", usedBuckets=" + usedBuckets()
                    + ", maxBucketSize=" + maxBucketSize()
                    + ", insertTimeSeconds=" + String.format("%.6f", elapsedSeconds));
        }
    }

    static List<String> generateRandomKeys(int n) {
        Random r = new Random(42);
        List<String> list = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            char[] chars = new char[8];
            for (int j = 0; j < 8; j++) chars[j] = (char)('a' + r.nextInt(26));
            list.add(new String(chars));
        }
        return list;
    }

    static List<String> generateSequentialKeys(int n) {
        List<String> list = new ArrayList<>();
        for (int i = 0; i < n; i++) list.add("user" + i);
        return list;
    }

    static List<String> generateClusteredKeys(int n) {
        List<String> list = new ArrayList<>();
        for (int i = 0; i < n; i++) list.add("aaa" + i);
        return list;
    }

    static void runExperiment(String name, List<String> keys, int tableSize) {
        System.out.println("\n--- " + name + " ---");
        for (String strat : new String[]{"sum", "polynomial"}) {
            HashTableChaining ht = new HashTableChaining(tableSize, strat);
            long start = System.nanoTime();
            for (int i = 0; i < keys.size(); i++) ht.insert(keys.get(i), i);
            double time = (System.nanoTime() - start) / 1e9;
            ht.printReport(time);
        }
    }

    public static void main(String[] args) {
        int n = 1000, tableSize = 211;
        runExperiment("Random", generateRandomKeys(n), tableSize);
        runExperiment("Sequential", generateSequentialKeys(n), tableSize);
        runExperiment("Clustered", generateClusteredKeys(n), tableSize);
    }
}