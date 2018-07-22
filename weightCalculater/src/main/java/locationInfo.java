import com.google.maps.GeoApiContext;
import com.google.maps.NearbySearchRequest;
import com.google.maps.errors.ApiException;
import com.google.maps.model.LatLng;
import com.google.maps.model.PlaceType;
import com.google.maps.model.PlacesSearchResponse;

import java.io.IOException;

public class locationInfo {
    public LatLng location;
    public double lat;
    public double lgt;
    public double cars;
    public double people;
    public double weight;

    public static final String API_KEY = "";
    public static final PlaceType[] PLACE_TYPES = {PlaceType.BANK, PlaceType.SUBWAY_STATION, PlaceType.PARK, PlaceType.HOSPITAL, PlaceType.STORE};
    public static final int[] WEIGHTS = {5, 10, 7, 7, 8};


    GeoApiContext context = null;
    public locationInfo(double lat, double lgt, double cars, double people) throws InterruptedException, ApiException, IOException {
        this.lat = lat;
        this.lgt = lgt;
        this.cars = cars;
        this.people = people;
        this.location = new LatLng(lat, lgt);
        weight = 0;
    }

    public void setWeight() throws InterruptedException, ApiException, IOException {
        this.weight = getWeightOfLocation(this.location) * 0.4 + 0.6 * (0.4 * this.cars + 0.6 * this.people);
    }

    public int getWeightOfLocation(LatLng location) throws InterruptedException, ApiException, IOException {
        context = new GeoApiContext.Builder().apiKey(API_KEY).build();
        int weight = 0;
        for(int i = 0; i < PLACE_TYPES.length; i++){
            weight = weight + WEIGHTS[i] * getNearBySearchByType(location, PLACE_TYPES[i]);
        }
        return weight;
    }

    public int getNearBySearchByType(LatLng position, PlaceType pt) throws InterruptedException, ApiException, IOException {
        NearbySearchRequest nearbySearchRequest = new NearbySearchRequest(context);
        nearbySearchRequest.radius(500);
        nearbySearchRequest.location(position);
        nearbySearchRequest.type(pt);
        PlacesSearchResponse placesSearchResponse = nearbySearchRequest.await();
        int size = placesSearchResponse.results.length;
        //System.out.println(size);
        return size;
    }
}
