package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.example.demo.model.MonthlyQuota;

public interface MonthlyQuotaRepository extends JpaRepository<MonthlyQuota, Long> {
    MonthlyQuota findByAadhaar(String aadhaar);
}
