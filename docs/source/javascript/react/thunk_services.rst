============================
Using Services In Components
============================


This is The Correct Way
-----------------------

.. code-block:: javascript

  // Services
  export function createChannelSet (data) {
    return (dispatch) => {
      dispatch(Outputs.createChannelSet());
      return axios.post('/api/channel_set', data)
        .then(
          resp => {
            dispatch(Outputs.createChannelSetSuccess(resp.data));
            return resp;
          }
        )
        .catch(
          resp => {
            dispatch(Outputs.createChannelSetError(resp.data));
          }
        );
    };
  }

   // Component
   class OutputListView extends Component {
   
  
     submitCreateOutputRequest () {
       const { createChannelSet } = this.props.actions;
   
       createChannelSet(this.state.createOutputValues)
        .then((response) => {
          browserHistory.push(`/outputs/${response.data.createdOutput.id}/channels`);
        });
     }

   }

This is the cleanest way to execute follow-up code for a component after calling a service.

Because the service returns the promise, the react component can chain ``.then`` off the end of the promise and give it actions to complete based on the results of the service.

This requires no code at all in ``componentWillReceiveProps``.

Note that for the any chained ``.then`` methods to access the response the earlier ``.then`` methods must return that object.


This Is Okay
------------

.. code-block:: javascript


   // Services
   export function createChannelSet (data) {
   return (dispatch) => {
     dispatch(Outputs.createChannelSet());
     axios.post('/api/channel_set', data)
       .then(
         resp => {
           dispatch(Outputs.createChannelSetSuccess(resp.data));
         }
       )
       .catch(
         resp => {
           dispatch(Outputs.createChannelSetError(resp.data));
         }
       );
     };
   }

   // Component
   class OutputListView extends Component {
   
     componentWillReceiveProps (nextProps) {
       if (!this.props.output !== nextProps.output && !nextProps.isRequesting) {
         browserHistory.push(`/outputs/${nextProps.output.id}/channels`);
       }
     }
   
     submitCreateOutputRequest () {
       const { createChannelSet } = this.props.actions;
   
       createChannelSet(this.state.createOutputValues);
     }

   }

What's good about this method is that all of a components redux related actions are contained in one area.

However, this can get pretty messy in ``componentWillReceiveProps``, and comparing ``this.props`` and ``nextProps`` doesn't always hold up with react router, because there might be leftover props from earlier (maybe not in this example but some situations).


This is bad
-----------

.. code-block:: javascript

   // Services
   export function createChannelSet (data, redirect = False) {
   return (dispatch) => {
     dispatch(Outputs.createChannelSet());
     axios.post('/api/channel_set', data)
       .then(
         resp => {
           dispatch(Outputs.createChannelSetSuccess(resp.data));

           if (redirect) {
             browserHistory.push(`/outputs/${nextProps.output.id}/channels`);
           }
         }
       )
       .catch(
         resp => {
           dispatch(Outputs.createChannelSetError(resp.data));
         }
       );
     };
   }

   // Component
   class OutputListView extends Component {
   
     submitCreateOutputRequest () {
       const { createChannelSet } = this.props.actions;
   
       createChannelSet(this.state.createOutputValues, true);
     }
   }


This is bad for several reasons:

#. The ``thunk`` service should only be responsible for making it's AJAX calls and hitting the corrosponding redux actions, so nothing unexpected is happening while trying to trigger actions.
#. The ordering of execution isn't liner in JavaScript; it might mess with things if the redirect occurs before the action is dispatched.
