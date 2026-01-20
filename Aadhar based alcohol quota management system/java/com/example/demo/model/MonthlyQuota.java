package com.example.demo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "monthly_quota")
public class MonthlyQuota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String aadhaar;
    private int allowedBottles;
    private int remainingBottles;
    private String monthYear;

    public Long getId() { return id; }
    public String getAadhaar() { return aadhaar; }
    public int getAllowedBottles() { return allowedBottles; }
    public int getRemainingBottles() { return remainingBottles; }
    public String getMonthYear() { return monthYear; }

    public void setId(Long id) { this.id = id; }
    public void setAadhaar(String aadhaar) { this.aadhaar = aadhaar; }
    public void setAllowedBottles(int allowedBottles) { this.allowedBottles = allowedBottles; }
    public void setRemainingBottles(int remainingBottles) { this.remainingBottles = remainingBottles; }
    public void setMonthYear(String monthYear) { this.monthYear = monthYear; }
}

