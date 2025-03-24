import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  ChakraProvider,
  Box,
  Heading,
  Select,
  Input,
  Button,
} from "@chakra-ui/react";

const App = () => {
  const [therapistTypes, setTherapistTypes] = useState([]);
  const [selectedType, setSelectedType] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(true);

  // Backend API URL
  const API_URL = "http://192.168.1.105:8001";

  // Fetch therapist types from backend
  useEffect(() => {
    axios
      .get(`${API_URL}/therapist-types`)
      .then((response) => {
        console.log("Therapist types loaded:", response.data.therapist_types);
        setTherapistTypes(response.data.therapist_types);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching therapist types:", error.message);
        setLoading(false);
      });
  }, []);

  const handleSearch = () => {
    console.log("Searching for:", selectedType, location);
    // Here, you'd make an API request to get search results based on user inputs
  };

  return (
    <ChakraProvider>
      <Box textAlign="center" p={6} maxW="400px" mx="auto">
        <Heading mb={4}>Find a Therapist</Heading>

        {/* Therapist Type Dropdown */}
        <Select
          placeholder={loading ? "Loading therapist types..." : "Select therapist type"}
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value)}
          mb={3}
          isDisabled={loading}
        >
          {therapistTypes.map((type, index) => (
            <option key={index} value={type}>
              {type}
            </option>
          ))}
        </Select>

        {/* Location Input */}
        <Input
          placeholder="Enter location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          mb={3}
        />

        {/* Search Button */}
        <Button colorScheme="blue" onClick={handleSearch} isDisabled={loading}>
          Search
        </Button>
      </Box>
    </ChakraProvider>
  );
};

export default App;
