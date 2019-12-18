import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;





public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String csvFile="../imageoutput.csv";
		BufferedReader br=null;
		String lime ="";
		String cvsSplitBy=",";
		try {
			br=Files.newBufferedReader(Paths.get(csvFile));
			Charset.forName("UTF-8");
	}

}
