import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setTodoList,
  updateTodo,
  sortTodo,
  toggleCompleted,
} from "../ToDoSlice";
import { TiPencil } from "react-icons/ti";
import { BsHddNetwork, BsTrash } from "react-icons/bs";
import empty from "../assets/empty.jpg";
import "../index.css";
import { useNavigate } from "react-router-dom";

const ToDoList = () => {
  const dispatch = useDispatch();
  const todoList = useSelector((state) => state.todo.todoList);
  const sortCriteria = useSelector((state) => state.todo.sortCriteria);
  const accessToken = useSelector((state) => state.auth.access_token);
  const [showModal, setShowModal] = React.useState(false);
  const [currentTodo, setCurrentTodo] = React.useState(null);
  const [newTask, setNewTask] = React.useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!accessToken) {
      alert("Please login first");
      navigate("/login");
    } else {
      fetchData();
    }
  }, []);

  // useEffect(() => {
  //   navigate("/login");
  // }, [accessToken]);

  const fetchData = () => {
    fetch("http://localhost:8000/todos/", {
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const todoArray = data.map((item) => ({
          task: item.content,
          id: item.id,
          completed: item.is_done,
        }));
        dispatch(setTodoList(todoArray));
        console.log(todoArray);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const addData = (props) => {
    fetch("http://localhost:8000/todos/", {
      method: "POST",
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(props),
    })
      .then((response) => response.json())
      .then(() => {
        fetchData();
      });
  };

  const deleteData = (id) => {
    fetch(`http://localhost:8000/todos/${id}/`, {
      method: "DELETE",
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    })
      .then(() => {
        fetchData();
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleAddTodo = (task) => {
    if (task.trim().length === 0) {
      alert("please enter a task");
    } else {
      addData({
        content: task,
        is_done: false,
      });

      setNewTask("");
      setShowModal(true);
    }
  };
  const handleUpdateTodoList = (id, task) => {
    if (task.trim().length === 0) {
      alert("please enter a task");
    } else {
      dispatch(updateTodo({ task: task, id: id }));
      setShowModal(false);
    }
  };
  const handleDeleteToDo = (id) => {
    deleteData(id);
  };

  const handleSort = (sortCriteria) => {
    dispatch(sortTodo(sortCriteria));
  };
  const sortTodoList = todoList.filter((todo) => {
    if (sortCriteria === "All") return true;
    if (sortCriteria === "Completed" && todo.completed) return true;
    if (sortCriteria === "Not Completed" && !todo.completed) return true;
    return false;
  });
  const handleToggleCompleted = (id) => {
    dispatch(toggleCompleted({ id }));
  };
  return (
    <div>
      {showModal && (
        <div className="fixed w-full left-0 top-0 h-full bg-transparentBlack flex justify-center items-center">
          <div className="bg-white p-8 rounded-md">
            <input
              type="text"
              className="border p-2 rounded-md outlinw-none mb-8"
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
              placeholder={
                currentTodo ? "Update your task here" : "Enter your task here"
              }
            />
            <div className="flex justify-between">
              {currentTodo ? (
                <>
                  <button
                    className="bg-sunsetOrange rounded-md text-white py-3 px-10"
                    onClick={() => {
                      setShowModal(false);
                      handleUpdateTodoList(currentTodo.id, newTask);
                    }}
                  >
                    Save
                  </button>
                  <button
                    className="bg-Tangaroa rounded-md text-white py-3 px-10"
                    onClick={() => setShowModal(false)}
                  >
                    Cancel
                  </button>
                </>
              ) : (
                <>
                  <button
                    className="bg-Tangaroa rounded-md text-white py-3 px-10"
                    onClick={() => {
                      setShowModal(false);
                    }}
                  >
                    Cancel
                  </button>
                  <button
                    className="bg-sunsetOrange rounded-md text-white py-3 px-10"
                    onClick={() => {
                      handleAddTodo(newTask);
                      setShowModal(false);
                    }}
                  >
                    Add
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
      <div className="flex items-center justify-center flex-col">
        {todoList.length === 0 ? (
          <div className="mb-8">
            <div className="sm:w-[500px] sm:h-[500px] min-w-[250px]">
              <img src={empty} alt="" />
            </div>
            <p className="text-center text-Gray">
              You have no todo's,plese add one.
            </p>
          </div>
        ) : (
          <div className="container mx-auto mt-6">
            <div className="flex justify-center mb-6">
              <select
                onChange={(e) => handleSort(e.target.value)}
                className="p-1 outline-none text-sm"
              >
                <option value="All" className="text-sm">
                  All
                </option>
                <option value="Completed" className="text-sm">
                  Completed
                </option>
                <option value="Not Completed" className="text-sm">
                  Not Completed
                </option>
              </select>
            </div>
            <div>
              {sortTodoList.map((todo) => (
                <div
                  key={todo.id}
                  className="flex items-center justify-between mb-6 bg-Tangaroa mx-auto w-full md:w-[75%] rounded-md p-4"
                >
                  <div
                    className={`${
                      todo.completed
                        ? "line-through text-greenTeal"
                        : "text-sunsetOrange"
                    }`}
                    onClick={() => {
                      handleToggleCompleted(todo.id);
                    }}
                  >
                    {todo.task}
                  </div>
                  <div>
                    <button
                      className="bg-blue-500 text-white p-1 rounded-md ml-2"
                      onClick={() => {
                        setShowModal(true);
                        setCurrentTodo(todo);
                        setNewTask(todo.task);
                      }}
                    >
                      <TiPencil />
                    </button>
                    <button
                      className="bg-sunsetOrange text-white p-1 rounded-md ml-2"
                      onClick={() => handleDeleteToDo(todo.id)}
                    >
                      <BsTrash />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <button
          className="bg-sunsetOrange text-center text-white py-3 px-10 rounded-md"
          onClick={() => setShowModal(true)}
        >
          Add Task
        </button>
      </div>
    </div>
  );
};

export default ToDoList;
