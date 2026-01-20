package com.example.demo.service;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.util.List;
import com.example.demo.repository.MonthlyQuotaRepository;
import com.example.demo.model.MonthlyQuota;

@Service
public class MonthlyResetService {

    private final MonthlyQuotaRepository repo;

    public MonthlyResetService(MonthlyQuotaRepository repo) {
        this.repo = repo;
    }

    // Runs on 1st day of every month at 00:00
    @Scheduled(cron = "0 0 0 1 * ?")
    public void resetMonthlyQuota() {

        List<MonthlyQuota> all = repo.findAll();
        String newMonth = LocalDate.now().getYear() + "-" +
                String.format("%02d", LocalDate.now().getMonthValue());

        for (MonthlyQuota q : all) {
            q.setRemainingBottles(q.getAllowedBottles());
            q.setMonthYear(newMonth);
            repo.save(q);
        }
    }
}

