package com.example.demo.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "registration")
public class Registration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private LocalDate dob;
    private String aadhaar;
    private String phone;
    private int bottles;

    public Long getId() { return id; }
    public String getName() { return name; }
    public LocalDate getDob() { return dob; }
    public String getAadhaar() { return aadhaar; }
    public String getPhone() { return phone; }
    public int getBottles() { return bottles; }

    public void setId(Long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setDob(LocalDate dob) { this.dob = dob; }
    public void setAadhaar(String aadhaar) { this.aadhaar = aadhaar; }
    public void setPhone(String phone) { this.phone = phone; }
    public void setBottles(int bottles) { this.bottles = bottles; }
}
