// matrix.hpp: exercise 12, a matrix whose invariant every operation keeps.
#pragma once
#include <cstddef>
#include <stdexcept>
#include <utility>
#include <vector>

class Matrix {
public:
    // Invariant: rows_ >= 1, cols_ >= 1 and data_.size() == rows_ * cols_.
    Matrix(std::size_t rows, std::size_t cols, double fill = 0.0)
        : rows_(rows), cols_(cols), data_(checked(rows, cols), fill) {}

    Matrix(const Matrix &) = default;
    Matrix &operator=(Matrix other) noexcept   // copy (or move) first, then swap: strong
    {
        std::swap(rows_, other.rows_);
        std::swap(cols_, other.cols_);
        data_.swap(other.data_);
        return *this;
    }

    std::size_t rows() const { return rows_; }
    std::size_t cols() const { return cols_; }
    double &operator()(std::size_t r, std::size_t c) { return data_[index(r, c)]; }
    double operator()(std::size_t r, std::size_t c) const { return data_[index(r, c)]; }

    Matrix transposed() const
    {
        Matrix t(cols_, rows_);
        for (std::size_t r = 0; r < rows_; r++)
            for (std::size_t c = 0; c < cols_; c++)
                t(c, r) = (*this)(r, c);
        return t;
    }
    Matrix operator*(const Matrix &o) const
    {
        if (cols_ != o.rows_)
            throw std::invalid_argument("sizes do not match");
        Matrix p(rows_, o.cols_);
        for (std::size_t r = 0; r < rows_; r++)
            for (std::size_t k = 0; k < cols_; k++)
                for (std::size_t c = 0; c < o.cols_; c++)
                    p(r, c) += (*this)(r, k) * o(k, c);
        return p;
    }

private:
    static std::size_t checked(std::size_t rows, std::size_t cols)
    {
        if (rows == 0 || cols == 0)
            throw std::invalid_argument("empty matrix");
        return rows * cols;
    }
    std::size_t index(std::size_t r, std::size_t c) const
    {
        if (r >= rows_ || c >= cols_)
            throw std::out_of_range("matrix index");
        return r * cols_ + c;
    }
    std::size_t rows_, cols_;
    std::vector<double> data_;
};
