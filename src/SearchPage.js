import React, { useState, useEffect } from "react";
import axios from "axios";
import { ChakraProvider, Box, Select, Input, Button, VStack, Text, Heading } from "@chakra-ui/react";

const SearchPage = () => {
  const [therapistTypes, setTherapistTypes] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [selectedSpecialty, setSelectedSpecialty] = useState("");
  const [location, setLocation] = useState("");

  // Fetch therapist types for dropdown
  useEffect(() => {
    axios.get("http://localhost:8001/therapist-types")
      .then((response) => setTherapistTypes(response.data.therapist_types))
      .catch((error) => console.error("Error fetching therapist types:", error));
  }, []);

  // Handle search request
  const handleSearch = () => {
    axios.get("http://localhost:8001/search", {
      params: { specialty: selectedSpecialty, location: location }
    })
      .then((response) => setSearchResults(response.data))
      .catch((error) => console.error("Error searching therapists:", error));
  };

  return (
    <ChakraProvider>
      <Box p={5} maxW="600px" mx="auto">
        <Heading mb={4}>Find a Therapist</Heading>
        <VStack spacing={4}>
          <Select placeholder="Select therapist type" onChange={(e) => setSelectedSpecialty(e.target.value)}>
            {therapistTypes.map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </Select>
          <Input placeholder="Enter location" value={location} onChange={(e) => setLocation(e.target.value)} />
          <Button colorScheme="blue" onClick={handleSearch}>Search</Button>
        </VStack>

        {searchResults.length > 0 && (
          <Box mt={6}>
            <Text fontSize="xl" fontWeight="bold">Results:</Text>
            {searchResults.map((therapist) => (
              <Box key={therapist.id} p={4} borderWidth="1px" borderRadius="lg" mt={2}>
                <Text fontSize="lg" fontWeight="bold">{therapist.name}</Text>
                <Text>{therapist.specialty} - {therapist.location}</Text>
                <Text fontSize="sm">{therapist.bio}</Text>
              </Box>
            ))}
          </Box>
        )}
      </Box>
    </ChakraProvider>
  );
};

export default SearchPage;
