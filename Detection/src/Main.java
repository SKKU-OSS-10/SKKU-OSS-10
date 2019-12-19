import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.ArrayList;
import java.io.InputStreamReader;




public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner user = new Scanner(System.in);
		System.out.print("Input your file path: ");
		String path = user.nextLine().trim();

		ProcessBuilder pb=new ProcessBuilder("python","detect_image.py",path);
		
		String csvoutput="output_modify.csv";
		BufferedReader br_init=null;
		String line ="";
		String cvsSplitBy=",";
		int[][][][] statistic=new int[6][64][7][64];
		for(int a=0;a<6;a++)
			for(int b=0;b<64;b++)
				for(int c=0;c<7;c++)
					for(int d=0;d<64;d++)
						statistic[a][b][c][d]=0;
		
		
		try {
			br_init=Files.newBufferedReader(Paths.get(csvoutput));
			Charset.forName("UTF-8");
			String prev[]=new String[12];

			int num=0;
			while((line=br_init.readLine())!=null) {
				List<String> temp=new ArrayList<String>();
				String array[]=line.split(cvsSplitBy);
				int curr=Integer.parseInt(array[0]);
				if(curr==num) {
					int color1=(Integer.parseInt(prev[7])/64)*16+(Integer.parseInt(prev[8])/64)*4+Integer.parseInt(prev[9])/64;
					int color2=(Integer.parseInt(array[7])/64)*16+(Integer.parseInt(array[8])/64)*4+Integer.parseInt(array[9])/64;
					int type1=Integer.parseInt(prev[6]);
					int type2=Integer.parseInt(array[6]);
					if(type1<type2) {
						if(type1>5) type1-=6;
						if(type2>5) type2-=6;
						statistic[type1][color1][type2][color2]+=5;
					}
					else {
						if(type1>5) type1-=6;
						if(type2>5) type2-=6;
						statistic[type2][color2][type1][color1]+=5;
					}
				}
				else {
					if(num!=0) {
						int color1=(Integer.parseInt(prev[7])/64)*16+(Integer.parseInt(prev[8])/64)*4+Integer.parseInt(prev[9])/64;
						int type1=Integer.parseInt(prev[6]);
						if(type1>5) {
							type1-=6;
							for(int i=0;i<64;i++)
								for(int j=0;j<6;j++) 
									statistic[j][i][type1][color1]++;
								
						}
						else {							
							for(int i=0;i<64;i++)
								for(int j=0;j<7;j++) 
									statistic[type1][color1][j][i]++;
								
						}
					}
					prev=array;
					num=curr;
				}
				
			}
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
		String image2[];
		int score=0;
		try {
			br=Files.newBufferedReader(Paths.get(csvFile));
			Charset.forName("UTF-8");
			line=br.readLine();
			image=line.split(cvsSplitBy);
			line=br.readLine();
			image2=line.split(cvsSplitBy);		
			int color1=(Integer.parseInt(image[7])/64)*16+(Integer.parseInt(image[8])/64)*4+Integer.parseInt(image[9])/64;
			int color2=(Integer.parseInt(image2[7])/64)*16+(Integer.parseInt(image2[8])/64)*4+Integer.parseInt(image2[9])/64;
			int type1=Integer.parseInt(image[6]);
			int type2=Integer.parseInt(image2[6]);
			if(type1<type2) {
				if(type1>5) type1-=6;
				if(type2>5) type2-=6;
				score=statistic[type1][color1][type2][color2];
			}
			else {
				if(type1>5) type1-=6;
				if(type2>5) type2-=6;
				score=statistic[type2][color2][type1][color1];
			}
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
		double max=0;
		for(int a=0;a<6;a++)
			for(int b=0;b<64;b++)
				for(int c=0;c<7;c++)
					for(int d=0;d<64;d++)
						if(max<statistic[a][b][c][d])
							max=statistic[a][b][c][d];
		score=(int)(score/max*100);
		System.out.println("Your Score is: "+score);
		
	}
}
