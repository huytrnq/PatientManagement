package it.unicas.action;

import com.opensymphony.xwork2.ActionSupport;
import org.apache.struts2.interceptor.SessionAware;
import org.apache.struts2.ServletActionContext;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Map;
import java.io.IOException;
import org.json.JSONArray;
import org.json.JSONObject;

public class SessionDataAction extends ActionSupport implements SessionAware {
    private Map<String, Object> session;
    private static final String DB_URL = "jdbc:mysql://localhost:3306/CareNet";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "Huytr1997";


    @Override
    public String execute() {
        JSONObject json = new JSONObject();
        
        try {

            String patientId = ServletActionContext.getRequest().getParameter("patientId");
            if (patientId != null) {
                // Fetch the patient data
                JSONObject patient = getPatientById(Integer.parseInt(patientId));
                json.put("patient", patient);
            }else{
                // Get the currently logged-in doctor from the session
                String doctorUsername = (String) session.get("username");
                
                // Fetch all patients who have appointments with the current doctor
                JSONArray patients = getPatientsByDoctor(doctorUsername);
                json.put("patients", patients);
            }

            // Return JSON response
            HttpServletResponse response = ServletActionContext.getResponse();
            response.setContentType("application/json");
            response.getWriter().write(json.toString());
            response.getWriter().flush();
            response.getWriter().close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return NONE; // No result page needed
    }

    private JSONArray getPatientsByDoctor(String doctorUsername) throws Exception {
        JSONArray patients = new JSONArray();
        
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT p.username, p.firstname, p.lastname, p.date_of_birth, a.status, p.id, p.insurance " +
                        "FROM user d " +
                        "JOIN appointment a ON d.id = a.doctor_id " +
                        "JOIN user p ON a.patient_id = p.id " +
                        "WHERE d.username = ?";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                stmt.setString(1, doctorUsername);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        JSONObject patient = new JSONObject();
                        patient.put("username", rs.getString("p.username"));
                        patient.put("firstname", rs.getString("p.firstname"));
                        patient.put("lastname", rs.getString("p.lastname"));
                        patient.put("status", rs.getString("a.status"));
                        patient.put("id", rs.getInt("p.id"));
                        patient.put("insurance", rs.getString("p.insurance"));
                        patient.put("dateOfBirth", rs.getDate("p.date_of_birth"));
                        patients.put(patient);
                    }
                }
            }
        }

        return patients;
    }

    private JSONObject getPatientById(int patientId) throws Exception {
        JSONObject patient = new JSONObject();
        // Implement logic to fetch patient data
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT * FROM user JOIN medical_info m ON user.id = m.user_id WHERE user.id = ?";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                stmt.setInt(1, patientId);
                try (ResultSet rs = stmt.executeQuery()) {
                    rs.next();
                    patient.put("risk_factor", rs.getString("risk_factor"));
                    patient.put("allergies", rs.getString("allergies"));
                    patient.put("last_surgery", rs.getString("last_surgery"));
                    patient.put("heart", rs.getString("heart"));
                    patient.put("blood_pressure", rs.getString("blood_pressure"));
                    patient.put("pulse", rs.getString("pulse"));
                    patient.put("abdomen", rs.getString("abdomen"));
                    patient.put("xray_path", rs.getString("xray_path"));
                    patient.put("ultrasound_path", rs.getString("ultrasound_path"));
                }
            }
        }
        return patient;
    }

    @Override
    public void setSession(Map<String, Object> session) {
        this.session = session;
    }
}