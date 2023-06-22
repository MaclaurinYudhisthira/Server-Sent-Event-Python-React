import React, { useEffect, useState } from "react";

function App() {
  const [notifications, setNotifications] = useState([]);
  const [userId, setUserId] = useState("");

  useEffect(() => {
    let eventSource;

    if(userId) {
      eventSource = new EventSource(`http://127.0.0.1:8000/api/v1/notifications/sse/${userId}`); // Replace "user123" with the actual user ID
      eventSource.onmessage = (event) => {
        console.log(event.data, "Event-data");
        // const notification = JSON.parse(event.data);
        // setNotifications((prevNotifications) => [notification, ...prevNotifications]);
      };
    }
     
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [userId]);

  return (
    <div>
      <h1>Notifications</h1>
      <label htmlFor="userID">
        <input type="text" name="userID" id="userID" onChange={({ target: { value }}) => {
          setUserId(value);
        }} 
        />
      </label>
      <ul>
        {notifications.map((notification) => (
          <li key={notification._id}>{notification.message}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
