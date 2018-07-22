import com.google.gson.*;
import com.google.maps.errors.ApiException;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Iterator;


public class getLocation {
    public static String fileName = "src/main/java/result_centers_weekend.json";
    public final static int COLUMN = 4;

    public static locationInfo[] getTopThree(double[][] metaLocation) throws InterruptedException, ApiException, IOException {
        int row = metaLocation.length;
        locationInfo[] locationInfos = new locationInfo[row];

        locationInfo[] rst = null;

        for(int i = 0; i < row; i++){
            locationInfos[i] = new locationInfo(metaLocation[i][1], metaLocation[i][0], metaLocation[i][2], metaLocation[i][3]);
            locationInfos[i].setWeight();
        }
        Arrays.sort(locationInfos, new Comparator<locationInfo>() {
            public int compare(locationInfo o1, locationInfo o2) {
                return (int)(o2.weight - o1.weight);
            }
        });

        rst = Arrays.copyOfRange(locationInfos, 0, 4);
        return rst;
    }

    public static void function(String fileName){
        JsonParser jsonParser = new JsonParser();
        try{
            FileReader fr = new FileReader(fileName);
            JsonElement json= jsonParser.parse(fr);
            JsonObject jsonObject = json.getAsJsonObject();
            int count = 0;
            for(String key : jsonObject.keySet()){

                if(count < 3){
                    count++;
                    continue;
                }
                double[][] location = getMetaLocation(key, jsonObject);
                locationInfo[] rst = getTopThree(location);
                //output
                for(locationInfo li : rst){
                    double[] aRst = {li.lgt, li.lat, li.weight};
                    System.out.println(Arrays.toString(aRst));
                }
            }

        }catch (JsonIOException e) {
            e.printStackTrace();
        } catch (JsonSyntaxException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ApiException e) {
            e.printStackTrace();
        }

    }

    public static double[][] getMetaLocation(String key, JsonObject jsonObject){
        double[][] arr = null;
        JsonArray jsonArray = jsonObject.get(key).getAsJsonArray();
        int size = jsonArray.size();
        arr = new double[size][COLUMN];
        for(int i = 0; i < jsonArray.size(); i++){
            double[] tmp = new double[COLUMN];
            JsonArray tmpJsonArray = jsonArray.get(i).getAsJsonArray();
            for(int j = 0; j < COLUMN; j++){
                JsonElement jsonElement = tmpJsonArray.get(j);
                tmp[j] = jsonElement.getAsDouble();
            }
                arr[i] = tmp;
            }
        return arr;
    }

    public static void main(String[] args) throws InterruptedException, ApiException, IOException {
        //double[][] location = {{-73.98516, 40.75686}, {-73.9775, 40.752796}, {-73.98037, 40.763294},{-73.97008, 40.762566}, {-73.97592, 40.745655}, {-73.9894, 40.76127}, {-73.969894, 40.755615}, {-73.99061, 40.750954}, {-73.99049, 40.74408}, {-73.98337, 40.745506}};
        //double[][] location = {{-73.98887, 40.763065, 1246.0}, {-73.970085, 40.75496, 1293.0}, {-73.98995, 40.75014, 1502.0}, {-73.97006, 40.76194, 1034.0}, {-73.98086, 40.763042, 1484.0}, {-73.98794, 40.757298, 1632.0}, {-73.98331, 40.745155, 1504.0}, {-73.990875, 40.744064, 1025.0}, {-73.9763, 40.74551, 1071.0}, {-73.97779, 40.75258, 1302.0}};
        //六小时1：double[][] location = {{-74.00112, 40.740936, 30525.0}, {-73.95364, 40.802746, 10160.0}, {-73.97646, 40.678917, 3777.0}, {-73.98181, 40.74651, 36375.0}, {-73.90447, 40.756485, 4337.0}, {-73.985275, 40.764297, 32944.0}, {-73.99318, 40.723125, 44158.0}, {-73.958435, 40.76811, 19070.0}, {-73.94714, 40.70923, 6441.0}, {-73.80229, 40.674587, 540.0}};
        //六小时2：double[][] location = {{-73.97989, 40.778816, 39151.0}, {-73.98098, 40.68655, 3672.0}, {-73.955826, 40.799896, 22276.0}, {-73.95655, 40.773243, 69935.0}, {-73.99437, 40.75177, 67971.0}, {-73.79008, 40.660923, 805.0}, {-73.98675, 40.736843, 60778.0}, {-73.901886, 40.757023, 3663.0}, {-73.97509, 40.757557, 103381.0}, {-74.005196, 40.721092, 37170.0}};
        function(fileName);

/*
        locationInfo[] rst = getTopThree(location);

        for(locationInfo li : rst){
                System.out.println(li.lgt + ", " + li.lat + ", " + li.weight);
        }
*/
    }
}
