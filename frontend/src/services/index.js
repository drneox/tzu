import axios from "axios";
export const updateThreatsRiskBatch = async (systemId, updates) => {
  return axios.put(`http://localhost:8000/information_systems/${systemId}/threats/risk/batch`, updates);
};

export const createThreatForSystem = async (systemId, threatData) => {
  return axios.post(`http://localhost:8000/information_systems/${systemId}/threats`, threatData);
};

export const fetchInformationSystemById = async (id) => {
  const res = await getInformationSystemsById(id);
  return res.data;
};
export const uploadDiagram = (id, file) => {
    const formData = new FormData();
    formData.append("file", file);
    return axios.post(`http://localhost:8000/evaluate/${id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
    });
};

export const getInformationSystems = () => {
    return axios.get("http://localhost:8000/information_systems/?skip=0&limit=100")
};

export const getInformationSystemsById = (id) => {
    return axios.get(`http://localhost:8000/information_systems/${id}`)
};

export const createInformationSystem = (data) => {
    return axios.post("http://localhost:8000/new", data);
};

