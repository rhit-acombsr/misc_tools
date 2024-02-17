package NthPrime;

import java.util.ArrayList;
//file in
import java.io.File;
import java.util.Scanner;
//file out
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
//system properties for filepaths
import java.util.Properties;

public class NthPrime {
    ArrayList<Integer> primes;
    String filePath;
    File dir;
    File PrimesTable;

    public NthPrime(){
        this.primes = new ArrayList<Integer>();
        this.primes.add(0,2);
        this.setFilePath();
    }

    public NthPrime(String filePath){
        Scanner s = new Scanner(new File(filePath));
        primes = new ArrayList<Integer>();
        while (s.hasNext()){
            if(s.hasNextInt())
                list.add(s.nextInt());
            else
                s.next();
        }
        this.filePath = filePath;
    }

    public void setFilePath(){
        String sagactic = File.separator+"Sagactik"+File.separator;
        String home = System.getProperty("user.home");
        this.filePath = home+sagactic+"NthPrime"+File.separator;
    }

    public void resetPrimesTable(){
        this.primes = new ArrayList<Integer>();
        System.out.println("Table Reset Successfully.");
    }

    public void savePrimesTable(){
        int attempt = 0;
        while(attempt < 3){
            try {
                FileWriter myWriter = new FileWriter(this.filePath+"primesTable.txt");
                for(Integer digit : this.primes){
                    myWriter.write(Integer.toString(digit) + " ");
                }
                // myWriter.write("content");
                myWriter.close();
                System.out.println("Table Written Successfully.");
                attempt = 3;
            } catch (FileNotFoundException e) {
                this.dir = new File(this.filePath);
                this.dir.mkdirs();
                attempt ++;
            } catch (IOException e) {
                System.out.println(e.getMessage());
                e.printStackTrace();
                System.exit(1);
            }
        }
    }

    public void loadPrimesTable(){
        Scanner scanner = null;
		this.PrimesTable = null;
        try {
			this.PrimesTable = new File(this.filePath+"primesTable.txt");
            scanner = new Scanner(this.PrimesTable);
            this.primes = new ArrayList<Integer>();
            while (scanner.hasNext()){
                if(scanner.hasNextInt())
                    this.primes.add(scanner.nextInt());
                else
                scanner.next();
            }
            System.out.println("Table Loaded Successfully.");
		} catch (FileNotFoundException e) {
			System.out.println(e.getMessage());
			File parentFolder = this.PrimesTable.getParentFile();
			System.out.println("Folder searched for the file not found: " + parentFolder.getAbsolutePath());
			System.exit(1);
		}
    }

    public boolean isPrimeBrute(int p){
        for(int i = 2;i<p;i++){
            if(p%i == 0)
                return false;
        }
        return true;
    }

    public int pGenBruteForce(int v){
        while((! this.isPrimeBrute(v))||(v<=this.primes.get(this.primes.size()-1)))
            v++;
        return v;
    }

    public void generateToNthPrime(int N){
        int p = this.primes.get(this.primes.size()-1);
        for(int n = this.primes.size(); n<N;n++){
            p = this.pGenBruteForce(p);
            this.primes.add(n,p);
        }
    }

    public int getNthPrime(int N){
        if(N<=this.primes.size())
            return this.primes.get(N-1);
        generateToNthPrime(N);
        this.savePrimesTable();
        return this.primes.get(N-1);
    }

    public static void main(String args[]) {
        NthPrime primeGen = new NthPrime();
        primeGen.generateToNthPrime(3);
        // System.out.println(primeGen.primes.toString());
        // primeGen.savePrimesTable();
        // System.out.println(primeGen.primes.toString());
        // primeGen.resetPrimesTable();
        // System.out.println(primeGen.primes.toString());
        // primeGen.loadPrimesTable();
        // System.out.println(primeGen.primes.toString());
        System.out.println(primeGen.getNthPrime(100000));
        // System.out.println(primeGen.primes.toString());
    }
}