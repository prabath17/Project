package com.example.demo.controller;

import java.time.LocalDate;
import java.time.Period;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import com.example.demo.repository.MonthlyQuotaRepository;
import com.example.demo.model.*;
import com.example.demo.repository.*;

@Controller
public class PageController {

    private final AdminRepository adminRepo;
    private final UserRepository userRepo;
    private final RegistrationRepository regRepo;
    private final MonthlyQuotaRepository monthlyRepo;

    public PageController(AdminRepository adminRepo,
                          UserRepository userRepo,
                          RegistrationRepository regRepo,
                          MonthlyQuotaRepository monthlyRepo) {

        this.adminRepo = adminRepo;
        this.userRepo = userRepo;
        this.regRepo = regRepo;
        this.monthlyRepo = monthlyRepo;
    }


    // HOME
    @GetMapping("/")
    public String home() {
        return "home";
    }

    // LOGIN
    @GetMapping("/login")
    public String login() {
        return "login";
    }

    @PostMapping("/login")
    public String loginCheck(@RequestParam String email,
                             @RequestParam String password,
                             Model model) {

        Admin admin = adminRepo.findByEmail(email);
        if (admin != null && password.equals(admin.getPassword())) {
            return "redirect:/signup";
        }

        User user = userRepo.findByEmail(email);
        if (user != null && password.equals(user.getPassword())) {
            return "redirect:/register";
        }

        model.addAttribute("error", "Invalid credentials");
        return "login";
    }

    // ADMIN → CREATE USER
    @GetMapping("/signup")
    public String signup(Model model) {
        model.addAttribute("user", new User());
        return "signup";
    }

    @PostMapping("/signup")
    public String saveUser(@ModelAttribute User user) {
        userRepo.save(user);
        return "signup";
    }

    // REGISTER PAGE
    @GetMapping("/register")
    public String register(Model model) {
        model.addAttribute("reg", new Registration());
        return "register";
    }



    @GetMapping("/validation")
    public String validationPage() {
        return "validation";
    }

    @PostMapping("/validate")
    public String validateAadhaar(@RequestParam String aadhaar, Model model) {

        if (!aadhaar.matches("\\d{12}")) {
            model.addAttribute("error", "Aadhaar must be exactly 12 digits");
            return "validation";
        }

        Registration reg = regRepo.findByAadhaar(aadhaar);
        if (reg == null) {
            model.addAttribute("error", "No record found for this Aadhaar number");
            return "validation";
        }

        MonthlyQuota quota = monthlyRepo.findByAadhaar(aadhaar);
        if (quota == null || quota.getRemainingBottles() <= 0) {
            model.addAttribute("error", "No bottles remaining for this month");
            return "validation";
        }

        int age = Period.between(reg.getDob(), LocalDate.now()).getYears();
        boolean ageValid = age >= 18;
        boolean bottleValid = quota.getRemainingBottles() > 0;

        model.addAttribute("name", reg.getName());
        model.addAttribute("age", age);
        model.addAttribute("bottles", quota.getRemainingBottles());
        model.addAttribute("ageValid", ageValid);
        model.addAttribute("bottleValid", bottleValid);

        return "dashboard";
    }

    @PostMapping("/register")
    public String saveRegistration(@ModelAttribute Registration reg) {

        regRepo.save(reg);

        MonthlyQuota quota = new MonthlyQuota();
        quota.setAadhaar(reg.getAadhaar());
        quota.setAllowedBottles(reg.getBottles());
        quota.setRemainingBottles(reg.getBottles());
        quota.setMonthYear(LocalDate.now().getYear() + "-" +
                String.format("%02d", LocalDate.now().getMonthValue()));

        monthlyRepo.save(quota);

        return "redirect:/validation";
    }



}
