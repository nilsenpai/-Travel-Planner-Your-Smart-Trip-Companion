import google.generativeai as genai
from serpapi import GoogleSearch
import streamlit as st

genai.configure(api_key="AIzaSyD3N6UOddiuHiCbPrc8B9iEn8PhZwaomaw")
st.title("Travel Planner Your Best Guide")


#user se le
departure_input = st.text_input("Where are you departing from? ")
arrival_input = st.text_input("Where are you going to? ")
outbound_date = st.date_input("Enter outbound date (YYYY-MM-DD): ")
return_date = st.date_input("Enter return date (YYYY-MM-DD): ")
adults = st.number_input("Number of adults for hotel stay: ")
budget_input = st.selectbox("Select Budget", ["Low", "Medium", "High", "Luxurious"])

def get_iata_code_with_gemini(location):
    prompt = f"What is the nearest major airport IATA code to '{location}'? Reply with only the 3-letter airport code."
    model = genai.GenerativeModel('gemini-2.0-flash')
    response1 = model.generate_content(prompt)
    return response1.text.strip().upper()


# gemini se code le
if st.button("Plan My Trip"):
    with st.spinner("Getting airport codes..."):
        departure_code = get_iata_code_with_gemini(departure_input)
        arrival_code = get_iata_code_with_gemini(arrival_input)

    with st.spinner("Fetching flights and hotels..."):
        # Serap ka istamal
        flight_params = {
            "engine": "google_flights",
            "departure_id": departure_code,
            "arrival_id": arrival_code,
            "outbound_date": outbound_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "currency": "INR",
            "hl": "en",
            "api_key": "92e07318fa9443ff6884a3b7ca2b4f4ff5636d703c9069dd24505c8e32fa9d11"
        }

        flight_search = GoogleSearch(flight_params)
        flight_results = flight_search.get_dict()

        hotel_params = {
            "engine": "google_hotels",
            "q": arrival_input + " Hotels",  # Search in the destination city
            "check_in_date": outbound_date.strftime("%Y-%m-%d"),
            "check_out_date": return_date.strftime("%Y-%m-%d"),
            "adults": int(adults),
            "currency": "INR",
            "hl": "en",
            "gl": "in",
            "api_key": "92e07318fa9443ff6884a3b7ca2b4f4ff5636d703c9069dd24505c8e32fa9d11"
        }
        hotel_search = GoogleSearch(hotel_params)
        hotel_results = hotel_search.get_dict()
    with st.spinner("Planning your tour..."):
        prompt1 = f"""
        You are a travel planner. Based on the following data:

        Flight Details:
        {flight_results}

        Hotel Details:
        {hotel_results}

        Budget Details:
        {budget_input}

        No of adults for hotel stay: {int(adults)}

        Create a complete travel itinerary. Include:
        - Arrival and departure days
        - Hotel check-in/check-out
        - Sightseeing suggestions
        - Estimated cab costs
        -Estimated food costs
        - Total cost calculation (flights + hotel + cabs + food)
        - Suggestions for restaurants or local food
        -Famous or viral places 
        -Do all this by according to the budget 
        -Optional travel tips (weather, culture, etc.)
        - Keep the tone friendly and helpful

         Currency: INR.
        """
    # Generate karega plan ko
    model1 = genai.GenerativeModel('gemini-2.0-flash')
    response = model1.generate_content(prompt1)

    st.success("Your travel plan is ready!")
    st.markdown(response.text)
