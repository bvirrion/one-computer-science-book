// expr.hpp (exercise 10): arithmetic expressions as a class hierarchy.
#pragma once
#include <map>
#include <memory>
#include <stdexcept>
#include <string>

class Expr {
public:
    virtual ~Expr() = default;
    virtual double eval(const std::map<std::string, double> &env) const = 0;
    virtual std::string str() const = 0;
    virtual std::unique_ptr<Expr> simplify() const = 0;   // a new, simpler tree
    virtual const double *constant() const { return nullptr; }   // its value if it is a number
};
using ExprPtr = std::unique_ptr<Expr>;

class Num : public Expr {
public:
    explicit Num(double v) : v_(v) {}
    double eval(const std::map<std::string, double> &) const override { return v_; }
    std::string str() const override
    {
        std::string s = std::to_string(v_);
        s.erase(s.find_last_not_of('0') + 1);       // 2.500000 -> 2.5, 3.000000 -> 3.
        if (s.back() == '.') s.pop_back();
        return s;
    }
    ExprPtr simplify() const override { return std::make_unique<Num>(v_); }
    const double *constant() const override { return &v_; }

private:
    double v_;
};

class Var : public Expr {
public:
    explicit Var(std::string n) : n_(std::move(n)) {}
    double eval(const std::map<std::string, double> &env) const override
    {
        auto it = env.find(n_);
        if (it == env.end()) throw std::out_of_range("unbound variable " + n_);
        return it->second;
    }
    std::string str() const override { return n_; }
    ExprPtr simplify() const override { return std::make_unique<Var>(n_); }

private:
    std::string n_;
};

class Binary : public Expr {                        // what Add and Mul share
public:
    Binary(ExprPtr l, ExprPtr r) : l_(std::move(l)), r_(std::move(r)) {}
    double eval(const std::map<std::string, double> &env) const override
    {
        return apply(l_->eval(env), r_->eval(env));
    }
    std::string str() const override { return "(" + l_->str() + " " + op() + " " + r_->str() + ")"; }
    ExprPtr simplify() const override
    {
        ExprPtr a = l_->simplify(), b = r_->simplify();
        if (a->constant() && b->constant())         // fold two numbers
            return std::make_unique<Num>(apply(*a->constant(), *b->constant()));
        return rebuild(std::move(a), std::move(b));
    }

protected:
    virtual double apply(double x, double y) const = 0;
    virtual const char *op() const = 0;
    virtual ExprPtr rebuild(ExprPtr a, ExprPtr b) const = 0;   // the identities of each operator
    ExprPtr l_, r_;
};

class Add : public Binary {
public:
    using Binary::Binary;

protected:
    double apply(double x, double y) const override { return x + y; }
    const char *op() const override { return "+"; }
    ExprPtr rebuild(ExprPtr a, ExprPtr b) const override
    {
        if (a->constant() && *a->constant() == 0) return b;     // 0 + e = e
        if (b->constant() && *b->constant() == 0) return a;     // e + 0 = e
        return std::make_unique<Add>(std::move(a), std::move(b));
    }
};

class Mul : public Binary {
public:
    using Binary::Binary;

protected:
    double apply(double x, double y) const override { return x * y; }
    const char *op() const override { return "*"; }
    ExprPtr rebuild(ExprPtr a, ExprPtr b) const override
    {
        for (const ExprPtr *e : {&a, &b})
            if ((*e)->constant() && *(*e)->constant() == 0)
                return std::make_unique<Num>(0);                // 0 * e = e * 0 = 0
        if (a->constant() && *a->constant() == 1) return b;     // 1 * e = e
        if (b->constant() && *b->constant() == 1) return a;     // e * 1 = e
        return std::make_unique<Mul>(std::move(a), std::move(b));
    }
};
