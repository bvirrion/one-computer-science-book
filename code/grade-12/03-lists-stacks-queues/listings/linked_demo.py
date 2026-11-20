from cell import Cell, from_list, to_list

head = Cell(3, Cell(1, Cell(4, Cell(1))))   # 3 -> 1 -> 4 -> 1 -> None
cell = head
while cell is not None:                     # walking: follow the links
    print(cell.value, end=" -> ")
    cell = cell.next
print(None)

head = Cell(9, head)                        # insert at the head: one new cell
print(to_list(head))
second = head.next
second.next = second.next.next              # remove the cell after 3: skip it
print(to_list(head))
print(to_list(from_list("abc")), to_list(from_list([])))
