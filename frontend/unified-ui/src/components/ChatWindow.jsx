import React from "react";
import { useState, useRef, useEffect } from "react";
import "./ChatWindow.css"

export default function ChatWindow() {

    const [flow, setFlow] = useState(null); // null | "ADD_BENEFICIARY" | "TRANSFER_FUNDS"
    const [beneficiaryData, setBeneficiaryData] = useState({});
    const [transferData, setTransferData] = useState({});
    const [messages, setMessages] = useState([
                                      {
                                       id: 1,
                                       sender: "chatbot",
                                       text: "Welcome to ABC Bank. How may i help you ?",
    
                                      }
                                      ]);

    const scrollRef= useRef(null);
    const [input, setInput]= useState(""); 
    const handleOptionClick = async (option, msgId) => {
    const { label, value } = option;

  
    setMessages(prev =>
          prev.map(m =>
            m.id === msgId
              ? {
                  ...m,
                  options: m.options.map(opt =>
                    opt.label === label ? { ...opt, visible: false } : opt
                  )
                }
              : m
          )
        );

 
  if(label==="Check Balance") {
    const bal = await fetch("/api/transfer/balance?user_id=customer" , {
                      method:"GET",
                      })

    const data= await bal.json()
    addBotMessage(`Available Balance is ${data.balance}`)       
    return;
    }

  if (label === "Add Beneficiary") {
      setFlow("ADD_BENEFICIARY");
      setMessages(prev => [
        ...prev,
        { id: Date.now(), sender: "chatbot", text: "Please enter beneficiary name:" }
      ]);
      return;
    }
  if (flow === "TRANSFER_FUNDS" && value) {
      handleTransferFlow(null, value);
      return;
    }
  if (label === "Transfer Funds") {
      setFlow("TRANSFER_FUNDS");

    const res = await fetch("/api/beneficiary/list", {
    headers: {
      Authorization: "Basic " + btoa("customer:pass")
    }
  });

  const data = await res.json();

  addBotMessage(
    "Select Beneficiary:",
    data.map(b => ({
      label: b.name,
      value: b
    }))
  );

  return;
}
};
   
    const addBotMessage = (text, options = null) => {
      setMessages(prev => [...prev,  {
      id: Date.now(),
      sender: "chatbot",
      text,
      options: options ? options.map(o => ({ ...o, visible: true })) : undefined
    }
  ]);
};

    const resetTransfer = () => {
        setTransferData({});
        setFlow(null);
      };

   const handleTransferFlow = async (input, selectedBeneficiary) => {

    if (!transferData.beneficiary) {
        setTransferData({ beneficiary: selectedBeneficiary });
        addBotMessage("Enter amount to transfer:");
        return;
    }

    if (!transferData.amount) {
       
    if (!input || input.trim() === "") {
        alert(" Please enter an amount");
        return;
    }

      const amount = Number(input);

    if (isNaN(amount)) {
        alert(" Amount must be a valid number");
        return;
    }

    if (amount <= 0) {
        alert(" Amount must be greater than zero");
        return;
    }

        setTransferData(prev => ({ ...prev, amount }));
        
        
        
        const res = await fetch("/api/transfer/validate", {
            method: "POST",
            headers : {"Content-Type": "application/json"},
            body: JSON.stringify({
                beneficiary: transferData.beneficiary,
                amount: Number(input),
                user_id: "customer"
            })
        });

        const result = await res.json();
        
        if (!result.allowed) {
            addBotMessage(` Transfer failed: ${result.reason}`);
            resetTransfer();
            return;
        }
        const exec = await fetch("/api/transfer/execute", {
            method: "POST",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify(result.payload)
        });
        
        

        const execRes = await exec.json();
        console.log("validation response", execRes)
        addBotMessage(`✅ Transfer successful. Txn ID: ${execRes.transaction_id} .${execRes.message} . Available blance after the transaction is : ${execRes.remaining_balance}`);
        resetTransfer();
    }
};


    const handleChange = (e) => {
        setInput(e.target.value)
    }
   
    const handleKeyDown = (e) => {
        if(e.key==="Enter" && !e.shiftKey){
            e.preventDefault();
            sendMessage();
        }

    }
   
   const handleAddBeneficiaryFlow = async (input) => {
         if (!beneficiaryData.name) {
          setBeneficiaryData({ name: input });
          addBotMessage("Please enter IBAN number:");
          return;
        }

        if (!beneficiaryData.iban) {
            setBeneficiaryData(prev => ({ ...prev, iban: input }));
            addBotMessage("Please enter Bank Name:");
            return;
        }

        if (!beneficiaryData.bank_name) {
            setBeneficiaryData(prev => ({ ...prev, bank_name: input }));
            addBotMessage("Please enter Country:");
            return;
        }

  
        const finalData = { ...beneficiaryData, country: input };

        await fetch("/api/beneficiary/add", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            Authorization: "Basic " + btoa("customer:pass")
            },
            body: JSON.stringify(finalData)
        });

        addBotMessage(" Beneficiary added successfully.");
        setBeneficiaryData({});
        setFlow(null);
    };

   
    const detectIntent = (text) => {
        const msg = text.toLowerCase();

        if (msg.includes("add") || msg.includes("beneficiary")) return "ADD_BENEFICIARY";
        if (msg.includes("transfer") || msg.includes("fund")) return "TRANSFER_FUNDS";
        if (msg.includes("balance") || msg.includes("available") || msg.includes("check")) return "CHECK_BALANCE";
        if (msg.includes("transaction") || msg.includes("transactions") || msg.includes("history") || msg.includes("statement")) return "TRANSACTION_HISTORY";

        return "UNKNOWN";
    };

    const sendMessage = async (externalMsg) => {
    const trimmedMsg = externalMsg ? externalMsg.trim() : input.trim();
    if (!trimmedMsg) return;

  
    const userMsg = {
    id: "user-" + Date.now(),
    sender: "user",
    text: trimmedMsg
  };

  setMessages(prev => [...prev, userMsg]);
  setInput("");

  
  if (flow === "ADD_BENEFICIARY") {
    handleAddBeneficiaryFlow(trimmedMsg);
    return;
  }

  if (flow === "TRANSFER_FUNDS") {
    handleTransferFlow(trimmedMsg);
    return;
  }

  
  const intent = detectIntent(trimmedMsg);

  
  if (intent === "CHECK_BALANCE") {
    const bal = await fetch(
      "/api/transfer/balance?user_id=customer"
    );
    const data = await bal.json();
    addBotMessage(`Available balance is ${data.balance}`);
    return;
  }

  if (intent === "ADD_BENEFICIARY") {
    setFlow("ADD_BENEFICIARY");
    addBotMessage("Please enter beneficiary name:");
    return;
  }

  if (intent === "TRANSFER_FUNDS") {
    setFlow("TRANSFER_FUNDS");

    const res = await fetch("/api/beneficiary/list", {
      headers: {
        Authorization: "Basic " + btoa("customer:pass")
      }
    });

    const data = await res.json();

    addBotMessage(
      "Select beneficiary:",
      data.map(b => ({
        label: b.name,
        value: b
      }))
    );
    return;
  }

  if (intent === "TRANSACTION_HISTORY") {
  try {
    const res = await fetch(
      "/api/transfer/history?user_id=customer&limit=10",
      { method : "GET",
        headers: {
          Authorization: "Basic " + btoa("customer:pass")
        }
      }
    );

    const data = await res.json();

    if (!data.transactions || data.transactions.length === 0) {
      addBotMessage("No recent transactions found.");
      return;
    }

    
    const txnText = data.transactions
      .map(
        (t, idx) =>
          `${idx + 1}. ${t.date} | ${t.type} ₹${t.amount} → ${t.beneficiary} (Txn ID: ${t.txn_id})`
      )
      .join("\n");

    addBotMessage(` Last 10 Transactions:\n\n${txnText}`);
  } catch (err) {
    addBotMessage(" Unable to fetch transaction history right now.");
  }

  return;
}

  // llm call
if (intent === "UNKNOWN") {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Basic " + btoa("customer:pass")
      },
      body: JSON.stringify({
        msg: trimmedMsg
      })
    });

    const data = await res.json();
    addBotMessage(data.reply);
  } catch (err) {
    addBotMessage("Unable to process your request right now.");
  }
  return;
}
  
};

useEffect(()=> {
        if(scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight ;

        }
    },[messages]);


return(
    
        
      <div className="page-container">
        <div className="right-panel">
            <header className="right-header">
                <div className="div1-header"> ABC BANK CHATBOT</div>
                
            </header>
            <div className="chat-body" ref={scrollRef}>
               {messages.map(msg => (
  <div
    key={msg.id}
    className={`chat-message ${msg.sender === "user" ? "user" : "chatbot"}`}
  >
    <div className="message-content">
      {msg.text}

      {/* Render buttons if options exist */}
      {msg.options && (
  <div className="chat-options">
    {msg.options
      .filter(opt => opt.visible)
      .map((opt, index) => (
        <button
          key={index}
          className="option-btn"
          onClick={() => handleOptionClick(opt, msg.id)}
        >
          {opt.label}
        </button>
      ))}
  </div>
)}
    </div>
  </div>
))}

            </div>
            <div className="chat-input-container">
                <textarea className="chatinput-area" 
                placeholder="Type your Query here...."
                value={input}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                rows={1}
                />
                <button className="send-btn" onClick={() => sendMessage()}>Send </button>
            </div>


        </div>

     </div>


    
);


}