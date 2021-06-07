var quizQuestions = [
  {
      question: "What kind of housing is it?",
      answers: [
          {
              type: "HDB",
              content: "HDB"
          },
          {
              type: "Condo",
              content: "Condo"
          },
          {
              type: "Landed",
              content: "Landed"
          }
      ]
  },
  {
      question: "What is your budget?",
      answers: [
          {
              type: "1",
              content: "<$10K",
          },
          {
              type: "2",
              content: "$10K - $30K",
          },
          {
              type: "3",
              content: "$30K - $50K"
          },
          {
              type: "4",
              content: ">$50K"
          },
      ]
  },
  {
      question: "How much control do you want to hand to the Interior Designer?",
      answers: [
          {
              content: "Design everything for me.",
              type: "1"
          },
          {
              content: "I have some ideas.",
              type: "2"
          },
          {
              content: "I have a lot of ideas.",
              type: "3"
          },
      ]
  },
  {
      question: "What is your timeframe?",
      answers: [
          {
              content: "<1 month",
              type: "1"
          },
          {
              content: "1 - 2 months",
              type: "2"
          },
          {
              content: "2 - 3 months",
              type: "3"
          },
          {
              content: "> 3 months",
              type: "4"
          },
      ]
  },
];

export default quizQuestions;