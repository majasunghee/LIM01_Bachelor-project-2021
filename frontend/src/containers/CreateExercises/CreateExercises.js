import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Paper, MenuList, MenuItem, Button } from '@material-ui/core';
import Chip from '@material-ui/core/Chip';
import CreateForstaelse from '../../components/CreateForstaelse/CreateForstaelse';
import CreateChat from '../../components/CreateChat/CreateChat';
import CreateRyddeSetninger from '../../components/CreateRyddeSetninger';
import useStyles from './styles';
import { axiosInstance, axiosInstanceDelete } from '../../helpers/ApiFunctions';

const CreateExercises = () => {
  const classes = useStyles();
  const [step, setStep] = useState('Menu');
  const [forstaelseCount, setForstaelseCount] = useState(0);
  const [chatCount, setChatCount] = useState(0);
  const [ryddeSetningerCount, setRyddeSetningerCount] = useState(0);
  const [playId, setPlayId] = useState(0);
  const [forstaelseList] = useState([null, null, null, null, null]);
  const [chatList] = useState([null, null, null, null, null]);
  const [ryddeSetningerList] = useState([null, null, null, null, null]);
  const [emptySetError, setEmptySetError] = useState(null);
  const [editId, setEditId] = useState(null);
  const [formDataEdit, setFormDataEdit] = useState(null);
  const [currentExercise, setCurrentExercise] = useState(null);

  /**
   * This function is called after an exercise has been created backend. It
   * adds the exercise id to the set list and increments the counter for that exercise type.
   * @param {*} id the id for the exercise that has been created
   * @param {*} type what type of exercise it is
   */
  function updateFormData(id, type) {
    if (type === 1) {
      forstaelseList[forstaelseCount] = id;
      setForstaelseCount(forstaelseCount + 1);
    } else if (type === 2) {
      chatList[chatCount] = id;
      setChatCount(chatCount + 1);
    } else {
      ryddeSetningerList[ryddeSetningerCount] = id;
      setRyddeSetningerCount(ryddeSetningerCount + 1);
    }
  }

  /**
   * The function is used to retrieve the data from the exercise the user wants to edit.
   * It saves the return data and if in local states
   * which is passed as prop to the corresponding create Exercise type.
   * @param {*} id id for the exercise which will be edited
   * @param {*} exerciseType type of exercise to be edited
   */
  function editExercise(id, exerciseType) {
    axiosInstance
      .get(`/${exerciseType}/${id}`)
      .then((res) => {
        setFormDataEdit(res.data);
        setCurrentExercise(exerciseType);
        setEditId(id);
      })
      .catch((e) => {
        return e;
      });
  }

  // used to change step correctly when a user wants to edit an exercise
  useEffect(() => {
    if (editId !== null) {
      setStep(currentExercise);
    }
  }, [editId]);

  function setExercise(step) {
    setEmptySetError(null);
    setStep(step);
  }

  function postContent() {
    if (forstaelseCount === 0 && chatCount === 0 && ryddeSetningerCount === 0) {
      setEmptySetError(
        'Du må legge til minst en oppgave for å opprette et sett.'
      );
    } else {
      axiosInstance
        .post('/createsets/', {
          forstaelse1: forstaelseList[0],
          forstaelse2: forstaelseList[1],
          forstaelse3: forstaelseList[2],
          forstaelse4: forstaelseList[3],
          forstaelse5: forstaelseList[4],
          chat1: chatList[0],
          chat2: chatList[1],
          chat3: chatList[2],
          chat4: chatList[3],
          chat5: chatList[4],
          ryddeSetninger1: ryddeSetningerList[0],
          ryddeSetninger2: ryddeSetningerList[1],
          ryddeSetninger3: ryddeSetningerList[2],
          ryddeSetninger4: ryddeSetningerList[3],
          ryddeSetninger5: ryddeSetningerList[4],
        })
        .then((response) => {
          setPlayId(response.data.id);
          setStep('confirmation');
        })
        .catch((e) => {
          return e;
        });
    }
  }

  function onDelete(id, type, url) {
    axiosInstanceDelete
      .delete(url)
      .then(() => {
        if (type === 1) {
          chatList[chatList.indexOf(id)] = null;
          setChatCount(chatCount - 1);
        } else if (type === 2) {
          forstaelseList[forstaelseList.indexOf(id)] = null;
          setForstaelseCount(forstaelseCount - 1);
        } else {
          ryddeSetningerList[ryddeSetningerList.indexOf(id)] = null;
          setRyddeSetningerCount(ryddeSetningerCount - 1);
        }
      })
      .catch((e) => {
        return e;
      });
  }

  switch (step) {
    case 'Menu':
      return (
        <div className={classes.root}>
          <Paper className={classes.menu}>
            <h1>Velg oppgavetype</h1>
            <MenuList>
              <MenuItem
                disabled={chatCount > 4}
                onClick={() => setStep('chat')}
              >
                Chat
              </MenuItem>
              <MenuItem
                disabled={forstaelseCount > 4}
                onClick={() => setExercise('forstaelse')}
              >
                Forståelse
              </MenuItem>
              <MenuItem
                disabled={ryddeSetningerCount > 4}
                onClick={() => setExercise('rydde_setninger')}
              >
                Rydde Setninger
              </MenuItem>
            </MenuList>
            {emptySetError && <h4>{emptySetError}</h4>}
            <Button
              variant="contained"
              color="secondary"
              onClick={postContent}
              fullWidth
            >
              Opprett
            </Button>
          </Paper>
          <Paper className={classes.menu}>
            <h4>Øvelser:</h4>
            {chatList.map((id) => {
              if (id !== null) {
                return (
                  <Chip
                    label="Chat"
                    onDelete={() => onDelete(id, 1, `/deletechat/${id}`)}
                    onClick={() => editExercise(id, 'chat')}
                  />
                );
              }
              return <></>;
            })}
            {forstaelseList.map((id) => {
              if (id !== null) {
                return (
                  <Chip
                    label="Forstaelse"
                    onDelete={() => onDelete(id, 2, `/deleteforstaelse/${id}`)}
                    onClick={() => editExercise(id, 'forstaelse')}
                  />
                );
              }
              return <></>;
            })}
            {ryddeSetningerList.map((id) => {
              if (id !== null) {
                return (
                  <Chip
                    label="Rydde Setninger"
                    onDelete={() =>
                      // eslint-disable-next-line prettier/prettier
                      onDelete(id, 3, `/delete_rydde_setninger/${id}`)}
                    onClick={() => editExercise(id, 'rydde_setninger')}
                  />
                );
              }
              return <></>;
            })}
          </Paper>
        </div>
      );
    case 'chat':
      return (
        <CreateChat
          updateFormData={updateFormData}
          setStep={setStep}
          editId={editId}
          formDataEdit={formDataEdit}
          setEditId={setEditId}
        />
      );
    case 'forstaelse':
      return (
        <CreateForstaelse
          updateFormData={updateFormData}
          setStep={setStep}
          editId={editId}
          formDataEditForstaelse={formDataEdit}
          setEditId={setEditId}
        />
      );
    case 'rydde_setninger':
      return (
        <CreateRyddeSetninger
          updateFormData={updateFormData}
          setStep={setStep}
          editId={editId}
          formDataEdit={formDataEdit}
          setEditId={setEditId}
        />
      );
    case 'confirmation':
      return (
        <div>
          <h1>
            Takk! Settet kan spilles med id:
            {playId}
          </h1>
          <Link to="/" className={classes.title}>
            Hjemmeside
          </Link>
        </div>
      );
    default:
      return <> </>;
  }
};

export default CreateExercises;
