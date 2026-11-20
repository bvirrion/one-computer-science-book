// tree.hpp (exercise 9): children owned by unique_ptr, parent observed by a raw pointer.
#pragma once
#include <memory>
#include <string>
#include <vector>

struct Node {
    std::string name;
    Node *parent = nullptr;                          // observes; never deletes
    std::vector<std::unique_ptr<Node>> children;     // owns

    explicit Node(std::string n) : name(std::move(n)) {}
    Node &add(std::string n)
    {
        children.push_back(std::make_unique<Node>(std::move(n)));
        children.back()->parent = this;
        return *children.back();
    }
    std::string path() const
    {
        return parent ? parent->path() + "/" + name : name;
    }
    // Moves the subtree rooted at child i under the node `to` (not inside that subtree).
    void move_child(std::size_t i, Node &to)
    {
        std::unique_ptr<Node> c = std::move(children[i]);
        children.erase(children.begin() + i);
        c->parent = &to;
        to.children.push_back(std::move(c));
    }
};
