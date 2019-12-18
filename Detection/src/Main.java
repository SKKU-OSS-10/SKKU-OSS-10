import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;





public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String csvoutput="output_modify.csv";
		BufferedReader br_init=null;
		String line ="";
		String cvsSplitBy=",";
		List<List<String>> set=new ArrayList<List<String>>();
		
		try {
			br_init=Files.newBufferedReader(Paths.get(csvoutput));
			Charset.forName("UTF-8");
	
			while((line=br_init.readLine())!=null) {
				List<String> temp=new ArrayList<String>();
				String array[]=line.split(cvsSplitBy);
				temp=Arrays.asList(array);
				System.out.println(temp.get(0));
				set.add(temp);
			}
			String array[]=line.split(cvsSplitBy);
		}catch(FileNotFoundException e) {
			e.printStackTrace();
		}catch(IOException e) {
			e.printStackTrace();
		}finally {
			try {
				if(br_init!=null) {
					br_init.close();
				}
			}catch(IOException e) {
				e.printStackTrace();
			}	
		}
		
		
		
		String csvFile="imageoutput.csv";
		BufferedReader br=null;
		String image[];
		try {
			br=Files.newBufferedReader(Paths.get(csvFile));
			Charset.forName("UTF-8");
			line=br.readLine();
			image=line.split(cvsSplitBy);
		}catch(FileNotFoundException e) {
			e.printStackTrace();
		}catch(IOException e) {
			e.printStackTrace();
		}finally {
			try {
				if(br!=null) {
					br.close();
				}
			}catch(IOException e) {
				e.printStackTrace();
			}	
		}
		
		
	}
}
