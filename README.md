# wiz light manual control
im not usually a smart home fan but these RGB bulbs that listen for api requests on lan are just pretty sick, as overengineered as stuffing a wifi + bluetooth esp in every bulb in my house is.       
         
I use the phillips' lower tier RGB bulbs, which use phillips' lighting but wiz for connectivity (wifi/bt, control, app, etc). I found this to be the best sweetspot because these are like THREE or FOUR times cheaper than phillips' top tier 'hue' line which uses their own connectivity. Though hue has a way better API, the app sucks, forces you to make an account, AND you cannot even create rooms or groups without buying another $60 bridge that's gotta wire into your network and sit on the wall. ???? all that for 3-4x the cost, and the same light quality as far as I can tell. I don't get it, am I missing something? why does everyone rave about phillips hue? if these bulbs die in a month or it comes out they're hard wired to the CCP, i'll come revise this opinion. till then, these things are great value.
             
anyway, these wiz connected bulbs have a very simple api interface that some people have already reverse engineered in the `pywizlight` python package. so naturally i want to mess with that, here is where i'll keep the experiments with that.           
          
sadly the dynamic color modes are all hardcoded in firmware and not configurable by the api. the api can only select one of the built in modes with an id, or, fade to a hex code / kelvin value. this is the downside from hue, but still, there are some fun things i can think to do, and some ways i think the app could better represent rooms and groups, at least for my purposes. 

## how the app represents rooms and groups
The wiz app is nicely simple, effective, no acct required, ad free, user friendly -- but the way it lets you group lights is a little limited.     
each light must belong to a room. rooms belong to a location (e.g. multiple houses). under one location, rooms are the top level group that any light must be a part of. you can control each light in a room individually, or you can control all lights in the room at once. within rooms, you can create groups: groups of devices that, once grouped, are now controlled as one device within the room. they are controlled together, but cannot be controlled individually any more.     
To put it in more formal CS terms: the program is limiting you to controlling the lights as a forest. The forest is limited to the following structure: the roots of the trees are different homes, layer 1 are the rooms in a home, layer 2 is either individual lights which are leaf nodes, or groups, with layer 3 then being the lights in a given group. The big limitation besides the fixed structure is: you cannot control from the root node, nor from layer 3. control can only be issued to either rooms (layer 1) or ungrouped lights / groups (layer 2).            


for my nerd purposes though i'd rather put less restrictions on the user facing data structs used to represent the lights.      
          
they could be a general tree. the root would be all the wiz lights I own. the first layer could be homes, the next layer rooms, the next layer groups (for multi bulb lamps etc), and layers below that would probably be rare. crucially, you could allow control from any node.

why limit it to a tree even? each house could just be a set of lights as nodes of a general graph, with directed edges representing a 'contains' like heirarchical relationship, and there can be non-light nodes used for grouping.

in fact, ^ that's maybe just an overengineered version of having the devices all be in a set, and all be taggable with arbitrary string tags, which then can be used to control all lights with a given tag at once. then groups can just overlap as the user pleases. to allow for an easier way to create a heirarchical relationship between tags, you could allow a tree of tags (e.g. create a tag that's a child of another, such that anything tagged with the child tag implicitly has the parent's tag).


idk, could be fun to mess with this at somepoint. it's a low priority, but i'll keep my work on it here

